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
    """DB 检测模型后处理：从概率图提取文本框，并合并为文本行"""

    def __init__(self, thresh=0.3, box_thresh=0.5, unclip_ratio=1.5,
                 use_polygon=False, min_size=3, max_candidates=1000,
                 merge_into_lines=True, merge_y_ratio=0.5):
        """
        Args:
            thresh: 二值化阈值
            box_thresh: 文本框分数阈值
            unclip_ratio: 框扩展系数
            use_polygon: 是否使用多边形轮廓（True）或最小外接矩形（False）
            min_size: 最小文本框尺寸
            max_candidates: 最大候选框数量
            merge_into_lines: 是否将相邻框合并为文本行
            merge_y_ratio: 合并阈值，y中心差异 < 框高 * 此值则视为同一行
        """
        self.thresh = thresh
        self.box_thresh = box_thresh
        self.unclip_ratio = unclip_ratio
        self.min_size = min_size
        self.max_candidates = max_candidates
        self.use_polygon = use_polygon
        self.merge_into_lines = merge_into_lines
        self.merge_y_ratio = merge_y_ratio

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

    def merge_boxes_into_lines(self, results):
        """
        将同一行中相邻的文本框合并成文本行框。

        改进策略（相比旧版贪心分组）：
        1. 每个 box 遍历所有已有行，选择 y 中心差异最小的行归入，
           而非只与"当前行"比较——避免因排序导致的错误分裂与级联误差。
        2. 判定同行的阈值用 min(box_h, line_h) * merge_y_ratio，
           比旧版滑动均值更稳定，避免大框拉松阈值后吞并邻行。
        3. x 方向间距检查：x 间距超过 5 倍行高时不合并，
           允许较大间距的同行框合并，减少框数接近 v3 行级输出。
        """
        if not results or len(results) <= 1:
            return results

        # 计算每个框的几何信息
        infos = []
        for r in results:
            box = np.array(r["box"], dtype=np.float32)
            y_center = float(np.mean(box[:, 1]))
            height = float(np.max(box[:, 1]) - np.min(box[:, 1]))
            x_min = float(np.min(box[:, 0]))
            x_max = float(np.max(box[:, 0]))
            y_min = float(np.min(box[:, 1]))
            y_max = float(np.max(box[:, 1]))
            infos.append({
                "box": box,
                "score": r["score"],
                "y_center": y_center,
                "height": max(height, 1.0),  # 避免除零
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
            })

        # 按 y 中心排序，再按 x 排序
        infos.sort(key=lambda b: (b["y_center"], b["x_min"]))

        # 行聚类：每个 box 尝试归入已有行，否则新建行
        lines = []  # 每个元素是 list of infos

        for b in infos:
            best_line_idx = -1
            best_y_diff = float('inf')

            for idx, line in enumerate(lines):
                # 当前行统计
                line_y_mean = float(np.mean([x["y_center"] for x in line]))
                line_h_mean = float(np.mean([x["height"] for x in line]))
                min_h = min(b["height"], line_h_mean)

                y_diff = abs(b["y_center"] - line_y_mean)

                # 判定条件1：y 中心差异小于两者最小高度 * merge_y_ratio
                if y_diff > min_h * self.merge_y_ratio:
                    continue

                # 判定条件2：x 方向间距不超过 5 倍行高（允许较大间距合并，减少框数）
                line_x_min = min(x["x_min"] for x in line)
                line_x_max = max(x["x_max"] for x in line)
                x_gap = max(0.0, max(b["x_min"] - line_x_max, line_x_min - b["x_max"]))
                if x_gap > line_h_mean * 5:
                    continue

                # 记录 y 差异最小的行
                if y_diff < best_y_diff:
                    best_y_diff = y_diff
                    best_line_idx = idx

            if best_line_idx >= 0:
                lines[best_line_idx].append(b)
            else:
                lines.append([b])

        # 合并每行的框为最小外接矩形
        merged = []
        for line in lines:
            if len(line) == 1:
                b = line[0]
                merged.append({"box": b["box"].tolist(), "score": b["score"]})
                continue

            all_pts = np.vstack([b["box"] for b in line])
            x_min = float(np.min(all_pts[:, 0]))
            x_max = float(np.max(all_pts[:, 0]))
            y_min = float(np.min(all_pts[:, 1]))
            y_max = float(np.max(all_pts[:, 1]))
            merged_box = [[x_min, y_min], [x_max, y_min],
                          [x_max, y_max], [x_min, y_max]]
            avg_score = float(np.mean([b["score"] for b in line]))
            merged.append({"box": merged_box, "score": avg_score})

        # 按行排序（从上到下），保证阅读顺序
        merged.sort(key=lambda r: float(np.mean(np.array(r["box"])[:, 1])))

        return merged

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

        # 合并相邻框为文本行（解决单字检测问题）
        if self.merge_into_lines and results:
            results = self.merge_boxes_into_lines(results)

        return results
