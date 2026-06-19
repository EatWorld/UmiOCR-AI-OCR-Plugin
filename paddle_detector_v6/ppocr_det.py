# -*- coding: utf-8 -*-
"""
PP-OCRv6 DB 文本检测 预处理与后处理
基于 PaddleOCR DB/DBNet 算法实现，仅做文本框检测，不做文本识别。

参考:
- https://github.com/PaddlePaddle/PaddleOCR
- https://github.com/RapidAI/RapidOCR
"""

import numpy as np
import cv2

try:
    import pyclipper
    from shapely.geometry import Polygon as ShapelyPolygon
    _HAS_SHAPELY = True
except ImportError:
    _HAS_SHAPELY = False


class DBPreProcess:
    """DB 检测模型预处理：缩放、归一化、转 CHW"""

    def __init__(self, limit_side_len=960, limit_type="max"):
        self.limit_side_len = limit_side_len
        self.limit_type = limit_type
        # ImageNet 标准归一化参数
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def resize_image(self, img):
        """等比缩放图片，使长边/短边不超过 limit_side_len，并 pad 到 32 的倍数。"""
        src_h, src_w = img.shape[:2]
        if self.limit_type == "max":
            if max(src_h, src_w) > self.limit_side_len:
                if src_h >= src_w:
                    ratio = float(self.limit_side_len) / src_h
                else:
                    ratio = float(self.limit_side_len) / src_w
            else:
                ratio = 1.0
        else:  # min
            if min(src_h, src_w) < self.limit_side_len:
                if src_h <= src_w:
                    ratio = float(self.limit_side_len) / src_h
                else:
                    ratio = float(self.limit_side_len) / src_w
            else:
                ratio = 1.0

        resize_h = int(round(src_h * ratio))
        resize_w = int(round(src_w * ratio))

        # 缩放
        if ratio != 1.0:
            img = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_LINEAR)

        # pad 到 32 的倍数
        pad_h = (32 - resize_h % 32) % 32
        pad_w = (32 - resize_w % 32) % 32
        if pad_h > 0 or pad_w > 0:
            img = cv2.copyMakeBorder(
                img, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(0, 0, 0)
            )

        return img, (src_h, src_w), (img.shape[0], img.shape[1])

    def normalize(self, img):
        """归一化: (img/255 - mean) / std"""
        img = img.astype(np.float32) / 255.0
        img = (img - self.mean) / self.std
        return img

    def to_chw(self, img):
        """HWC -> CHW"""
        return img.transpose((2, 0, 1))

    def __call__(self, img):
        """
        输入: BGR uint8 图片 (H, W, 3)
        输出: (tensor_data, original_size, resized_size)
            tensor_data: float32 (1, 3, H, W)
            original_size: (src_h, src_w)
            resized_size: (resized_h, resized_w)
        """
        resized, orig_size, resized_size = self.resize_image(img)
        normalized = self.normalize(resized)
        chw = self.to_chw(normalized)
        # 添加 batch 维度
        tensor = chw[np.newaxis, ...].astype(np.float32)
        return tensor, orig_size, resized_size


class DBPostProcess:
    """DB 检测模型后处理：从概率图提取文本框"""

    def __init__(self, thresh=0.3, box_thresh=0.6, unclip_ratio=1.5,
                 use_polygon=False, min_size=3, max_candidates=1000):
        """
        Args:
            thresh: 二值化阈值
            box_thresh: 文本框分数阈值
            unclip_ratio: 框扩展系数
            use_polygon: 是否使用多边形轮廓（True）或最小外接矩形（False）
            min_size: 最小文本框尺寸
            max_candidates: 最大候选框数量
        """
        self.thresh = thresh
        self.box_thresh = box_thresh
        self.unclip_ratio = unclip_ratio
        self.min_size = min_size
        self.max_candidates = max_candidates
        self.use_polygon = use_polygon

    def unclip(self, box):
        """使用 pyclipper 扩展多边形框"""
        try:
            poly = box.reshape(-1, 2)
            area = cv2.contourArea(poly.astype(np.int32))
            length = cv2.arcLength(poly.astype(np.int32), True)
            if length == 0:
                return None
            distance = area * self.unclip_ratio / length
            offset = pyclipper.PyclipperOffset()
            offset.AddPath(
                poly.tolist(),
                pyclipper.JT_ROUND,
                pyclipper.ET_CLOSEDPOLYGON,
            )
            expanded = offset.Execute(distance)
            if not expanded:
                return None
            expanded = np.array(expanded[0], dtype=np.float32)
            return expanded
        except Exception:
            return None

    def get_mini_boxes(self, contour):
        """获取最小外接矩形，返回4个角点和旋转角度"""
        rect = cv2.minAreaRect(contour)
        points = cv2.boxPoints(rect)
        points = np.sort(points, axis=0)
        index_1, index_2, index_3, index_4 = 0, 1, 2, 3
        if points[1][1] > points[0][1]:
            index_1 = 0
            index_4 = 1
        else:
            index_1 = 1
            index_4 = 0
        if points[3][1] > points[2][1]:
            index_2 = 2
            index_3 = 3
        else:
            index_2 = 3
            index_3 = 2

        box = np.array(
            [points[index_1], points[index_2], points[index_3], points[index_4]],
            dtype=np.float32,
        )
        return box, min(rect[1])

    def box_score_fast(self, bitmap, _box):
        """计算框内区域的平均概率分数"""
        h, w = bitmap.shape[:2]
        box = _box.copy()
        xmin = int(np.clip(np.floor(box[:, 0].min()), 0, w - 1))
        xmax = int(np.clip(np.ceil(box[:, 0].max()), 0, w - 1))
        ymin = int(np.clip(np.floor(box[:, 1].min()), 0, h - 1))
        ymax = int(np.clip(np.ceil(box[:, 1].max()), 0, h - 1))

        mask = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=np.uint8)
        box[:, 0] = box[:, 0] - xmin
        box[:, 1] = box[:, 1] - ymin
        cv2.fillPoly(mask, box.round().astype(np.int32)[np.newaxis, :, :], 1)
        return cv2.mean(bitmap[ymin:ymax + 1, xmin:xmax + 1], mask)[0]

    def __call__(self, preds, original_size, resized_size):
        """
        Args:
            preds: 模型输出 (1, 1, H, W) 或 (H, W) 概率图
            original_size: (src_h, src_w) 原始图片尺寸
            resized_size: (resized_h, resized_w) 缩放后尺寸（含 padding）

        Returns:
            list of boxes, 每个框为 4 点多边形 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            坐标已映射回原始图片尺寸
        """
        # 确保 preds 是 2D
        if isinstance(preds, (list, tuple)):
            preds = preds[0]
        if preds.ndim == 4:
            preds = preds[0, 0]
        elif preds.ndim == 3:
            preds = preds[0]

        src_h, src_w = original_size
        resized_h, resized_w = resized_size

        # 裁剪到原始缩放尺寸（去掉 padding 部分）
        preds = preds[:resized_h, :resized_w]
        # 缩放回原始尺寸
        pred = cv2.resize(preds, (src_w, src_h), interpolation=cv2.INTER_LINEAR)

        # 二值化
        bitmap = (pred > self.thresh).astype(np.uint8)

        # 查找轮廓
        contours, _ = cv2.findContours(
            bitmap, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        results = []
        for contour in contours[:self.max_candidates]:
            # 过滤太小的轮廓
            if contour.shape[0] < 4:
                continue
            area = cv2.contourArea(contour)
            if area < self.min_size * self.min_size:
                continue

            # 获取最小外接矩形
            box, sside = self.get_mini_boxes(contour)
            if sside < self.min_size:
                continue

            # 计算框内分数
            score = self.box_score_fast(pred, box)
            if score < self.box_thresh:
                continue

            # 扩展框
            expanded = self.unclip(box)
            if expanded is None:
                continue

            # 获取扩展后的最小外接矩形
            try:
                expanded_box, _ = self.get_mini_boxes(expanded.astype(np.int32))
            except Exception:
                continue

            # 确保坐标在图片范围内
            expanded_box[:, 0] = np.clip(expanded_box[:, 0], 0, src_w)
            expanded_box[:, 1] = np.clip(expanded_box[:, 1], 0, src_h)

            results.append({
                "box": expanded_box.tolist(),
                "score": float(score),
            })

        return results
