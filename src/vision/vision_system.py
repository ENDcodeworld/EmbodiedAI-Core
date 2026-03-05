"""
视觉系统核心模块
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from PIL import Image
import cv2


class VisionSystem:
    """
    视觉系统基类

    提供机器人视觉感知的基础功能，包括图像采集、预处理、
    特征提取和目标识别。

    Attributes:
        camera_id: 摄像头 ID
        resolution: 图像分辨率 (width, height)
        fps: 帧率
        is_active: 系统是否激活
    """

    def __init__(
        self,
        camera_id: int = 0,
        resolution: Tuple[int, int] = (640, 480),
        fps: int = 30,
    ) -> None:
        """
        初始化视觉系统

        Args:
            camera_id: 摄像头设备 ID
            resolution: 图像分辨率
            fps: 帧率
        """
        self.camera_id = camera_id
        self.resolution = resolution
        self.fps = fps
        self.is_active = False
        self._camera = None

    def initialize(self) -> bool:
        """
        初始化摄像头

        Returns:
            初始化是否成功
        """
        try:
            self._camera = cv2.VideoCapture(self.camera_id)
            if not self._camera.isOpened():
                return False
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self._camera.set(cv2.CAP_PROP_FPS, self.fps)
            self.is_active = True
            return True
        except Exception as e:
            print(f"初始化视觉系统失败：{e}")
            return False

    def capture_frame(self) -> Optional[np.ndarray]:
        """
        捕获单帧图像

        Returns:
            图像数组 (BGR 格式), 失败返回 None
        """
        if not self.is_active or self._camera is None:
            return None
        ret, frame = self._camera.read()
        return frame if ret else None

    def capture_rgb(self) -> Optional[np.ndarray]:
        """
        捕获 RGB 图像

        Returns:
            图像数组 (RGB 格式), 失败返回 None
        """
        frame = self.capture_frame()
        if frame is not None:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def shutdown(self) -> None:
        """关闭摄像头"""
        if self._camera is not None:
            self._camera.release()
            self._camera = None
        self.is_active = False

    def __enter__(self) -> "VisionSystem":
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.shutdown()
