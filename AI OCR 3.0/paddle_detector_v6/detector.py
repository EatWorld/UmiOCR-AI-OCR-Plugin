# -*- coding: utf-8 -*-
"""
PP-OCRv6 ONNX 检测器封装
仅做文本检测（分块），不做文本识别。
识别任务交给 AI 模型完成。

接口兼容旧版 PPOCR_umi.py 的 Api 类:
  - __init__(globalArgd)
  - start(argd) -> str ("" 成功, "[Error] xxx" 失败)
  - stop()
  - runBase64(imageBase64) -> {"code": 100, "data": [{"box": [...], "score": 1.0}]}
  - runPath(imgPath) -> 同上
  - runBytes(imageBytes) -> 同上

注意: 返回结果中 **不包含** "text" 字段，因为本模块仅负责检测，不负责识别。
"""

import os
import sys
import base64
import numpy as np

# 确保能导入 onnxruntime 和 pyclipper（bundled 在 libs 子目录）
_LIBS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs")
if _LIBS_DIR not in sys.path:
    sys.path.insert(0, _LIBS_DIR)

# 确保 Umi-OCR 的 site-packages 可用（numpy, cv2 等）
# 注意：在 Umi-OCR 主进程中，site-packages 已由 main.py 添加，无需额外处理。
# 但在独立测试时可能需要手动添加。

import cv2
import onnxruntime as ort

from .ppocr_det import DBPreProcess, DBPostProcess


class Api:
    """公开接口：PP-OCRv6 ONNX 文本检测器（仅检测）"""

    # 默认模型文件名
    DEFAULT_MODEL = "PP-OCRv6_det_small.onnx"

    def __init__(self, globalArgd):
        """
        Args:
            globalArgd: 全局参数字典，兼容旧版接口。
                        可选键: enable_mkldnn, cpu_threads, ram_max, ram_time,
                                limit_side_len, det_thresh, det_box_thresh,
                                det_unclip_ratio, det_model
        """
        self.global_config = dict(globalArgd) if globalArgd else {}
        self.session = None
        self.pre_process = None
        self.post_process = None
        self.isInit = True
        self._model_path = None

    def _find_model(self):
        """查找 ONNX 检测模型文件"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, "models")

        # 优先使用配置指定的模型
        model_name = self.global_config.get("det_model", self.DEFAULT_MODEL)
        model_path = os.path.join(models_dir, model_name)
        if os.path.isfile(model_path):
            return model_path

        # 回退：搜索 models 目录下任意 .onnx 文件
        if os.path.isdir(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith(".onnx"):
                    return os.path.join(models_dir, f)

        return None

    def start(self, argd):
        """启动检测引擎。返回 "" 成功，"[Error] xxx" 失败。"""
        if self.session is not None:
            return ""

        # 合并局部参数
        local = dict(argd) if argd else {}
        limit_side_len = int(local.get("limit_side_len",
                                       self.global_config.get("limit_side_len", 960)))

        # 查找模型
        model_path = self._find_model()
        if not model_path or not os.path.isfile(model_path):
            return f"[Error] 未找到 ONNX 检测模型文件。期望路径: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', self.DEFAULT_MODEL)}"
        self._model_path = model_path

        try:
            # 创建 ONNX Runtime 会话
            cpu_threads = int(self.global_config.get("cpu_threads", 0)) or None
            session_opts = ort.SessionOptions()
            if cpu_threads and cpu_threads > 0:
                session_opts.intra_op_num_threads = cpu_threads
                session_opts.inter_op_num_threads = 1
            # 图优化
            session_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

            self.session = ort.InferenceSession(
                model_path,
                sess_options=session_opts,
                providers=["CPUExecutionProvider"],
            )

            # 初始化预处理
            self.pre_process = DBPreProcess(
                limit_side_len=limit_side_len,
                limit_type="max",
            )

            # 初始化后处理
            # PP-OCRv6 默认参数
            thresh = float(local.get("det_thresh",
                                     self.global_config.get("det_thresh", 0.3)))
            box_thresh = float(local.get("det_box_thresh",
                                         self.global_config.get("det_box_thresh", 0.6)))
            unclip_ratio = float(local.get("det_unclip_ratio",
                                           self.global_config.get("det_unclip_ratio", 1.5)))

            self.post_process = DBPostProcess(
                thresh=thresh,
                box_thresh=box_thresh,
                unclip_ratio=unclip_ratio,
            )

            print(f"[AIOCR-detector-v6] 模型加载完成: {os.path.basename(model_path)}")
            print(f"[AIOCR-detector-v6] 参数: limit_side_len={limit_side_len}, "
                  f"thresh={thresh}, box_thresh={box_thresh}, unclip_ratio={unclip_ratio}")
            return ""
        except Exception as e:
            self.session = None
            return f"[Error] ONNX 检测器启动失败: {e}"

    def stop(self):
        """停止引擎"""
        self.session = None
        self.pre_process = None
        self.post_process = None

    def _detect(self, img):
        """
        对 BGR 图片执行检测。

        Returns:
            {"code": 100, "data": [{"box": [[x,y],...], "score": float}, ...]}
            {"code": 101, "data": "错误信息"}
        """
        if self.session is None:
            return {"code": 101, "data": "检测器未启动"}

        try:
            # 预处理
            tensor, orig_size, resized_size = self.pre_process(img)

            # 推理
            input_name = self.session.get_inputs()[0].name
            outputs = self.session.run(None, {input_name: tensor})

            # 后处理
            boxes = self.post_process(outputs[0], orig_size, resized_size)

            return {"code": 100, "data": boxes}
        except Exception as e:
            return {"code": 101, "data": f"检测异常: {e}"}

    def runPath(self, imgPath):
        """对本地图片文件进行检测"""
        if not os.path.isfile(imgPath):
            return {"code": 101, "data": f"图片文件不存在: {imgPath}"}
        img = cv2.imread(imgPath)
        if img is None:
            return {"code": 101, "data": f"无法读取图片: {imgPath}"}
        return self._detect(img)

    def runBytes(self, imageBytes):
        """对图片字节流进行检测"""
        try:
            img_array = np.frombuffer(imageBytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return {"code": 101, "data": "无法解码图片字节流"}
            return self._detect(img)
        except Exception as e:
            return {"code": 101, "data": f"图片字节流处理异常: {e}"}

    def runBase64(self, imageBase64):
        """对 base64 编码的图片进行检测"""
        try:
            # 处理 data URI 前缀
            if isinstance(imageBase64, str) and imageBase64.startswith("data:image"):
                imageBase64 = imageBase64.split(",", 1)[-1]
            image_bytes = base64.b64decode(imageBase64)
            return self.runBytes(image_bytes)
        except Exception as e:
            return {"code": 101, "data": f"base64 图片处理异常: {e}"}
