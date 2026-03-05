"""
视觉模块测试
"""

import pytest
import numpy as np
from PIL import Image
from embodiedai.vision import VisionSystem, ImageProcessor


class TestVisionSystem:
    """视觉系统测试"""

    def test_initialization(self):
        """测试初始化"""
        vs = VisionSystem(camera_id=0, resolution=(640, 480), fps=30)
        assert vs.camera_id == 0
        assert vs.resolution == (640, 480)
        assert vs.fps == 30
        assert vs.is_active is False

    def test_context_manager(self):
        """测试上下文管理器"""
        with VisionSystem() as vs:
            # 注意：实际测试中可能需要 mock 摄像头
            assert isinstance(vs, VisionSystem)


class TestImageProcessor:
    """图像处理器测试"""

    def setup_method(self):
        """测试前设置"""
        self.processor = ImageProcessor(default_size=(224, 224))
        self.test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    def test_resize(self):
        """测试图像缩放"""
        resized = self.processor.resize(self.test_image, (224, 224))
        assert resized.shape == (224, 224, 3)

    def test_normalize(self):
        """测试归一化"""
        normalized = self.processor.normalize(self.test_image)
        assert normalized.dtype == np.float32
        assert normalized.min() >= 0
        assert normalized.max() <= 1

    def test_to_tensor(self):
        """测试张量转换"""
        tensor = self.processor.to_tensor(self.test_image, channel_first=True)
        assert tensor.shape == (3, 480, 640)

        tensor = self.processor.to_tensor(self.test_image, channel_first=False)
        assert tensor.shape == (480, 640, 3)

    def test_preprocess_pipeline(self):
        """测试完整预处理流程"""
        result = self.processor.preprocess(
            self.test_image,
            resize_to=(224, 224),
            normalize=True,
            to_tensor=True,
        )
        assert result.shape == (3, 224, 224)
        assert result.dtype == np.float32

    def test_augment_flip(self):
        """测试翻转增强"""
        flipped = self.processor.augment(self.test_image, ["flip_horizontal"])
        assert flipped.shape == self.test_image.shape

    def test_augment_rotate(self):
        """测试旋转增强"""
        rotated = self.processor.augment(self.test_image, ["rotate_90"])
        assert rotated.shape == (640, 480, 3)
