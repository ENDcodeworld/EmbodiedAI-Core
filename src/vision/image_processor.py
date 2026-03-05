"""
图像处理器模块
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
from PIL import Image
import cv2


class ImageProcessor:
    """
    图像处理器

    提供图像预处理、增强、变换等功能。

    Attributes:
        default_size: 默认输出尺寸
        normalization: 是否进行归一化
    """

    def __init__(
        self,
        default_size: Optional[Tuple[int, int]] = (224, 224),
        normalization: bool = True,
    ) -> None:
        """
        初始化图像处理器

        Args:
            default_size: 默认输出尺寸 (width, height)
            normalization: 是否进行归一化
        """
        self.default_size = default_size
        self.normalization = normalization

    def resize(
        self,
        image: Union[np.ndarray, Image.Image],
        size: Optional[Tuple[int, int]] = None,
    ) -> np.ndarray:
        """
        调整图像大小

        Args:
            image: 输入图像
            size: 目标尺寸，默认使用 default_size

        Returns:
            调整大小后的图像
        """
        if size is None:
            size = self.default_size

        if isinstance(image, Image.Image):
            image = np.array(image)

        return cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)

    def normalize(
        self,
        image: np.ndarray,
        mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
        std: Tuple[float, ...] = (0.229, 0.224, 0.225),
    ) -> np.ndarray:
        """
        归一化图像

        Args:
            image: 输入图像 (0-255)
            mean: 均值
            std: 标准差

        Returns:
            归一化后的图像
        """
        if not self.normalization:
            return image.astype(np.float32) / 255.0

        image = image.astype(np.float32) / 255.0
        for i, (m, s) in enumerate(zip(mean, std)):
            image[:, :, i] = (image[:, :, i] - m) / s
        return image

    def to_tensor(
        self,
        image: np.ndarray,
        channel_first: bool = True,
    ) -> np.ndarray:
        """
        转换为张量格式

        Args:
            image: 输入图像
            channel_first: 是否将通道维度放在前面

        Returns:
            张量格式的图像
        """
        if channel_first:
            return np.transpose(image, (2, 0, 1))
        return image

    def preprocess(
        self,
        image: Union[np.ndarray, Image.Image, str],
        resize_to: Optional[Tuple[int, int]] = None,
        normalize: bool = True,
        to_tensor: bool = True,
    ) -> np.ndarray:
        """
        完整的图像预处理流程

        Args:
            image: 输入图像 (数组、PIL Image 或文件路径)
            resize_to: 调整到的尺寸
            normalize: 是否归一化
            to_tensor: 是否转换为张量

        Returns:
            预处理后的图像
        """
        # 加载图像
        if isinstance(image, str):
            image = Image.open(image)
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        # 调整大小
        if resize_to is not None:
            image = self.resize(image, resize_to)
        elif self.default_size is not None:
            image = self.resize(image, self.default_size)
        else:
            image = np.array(image)

        # 归一化
        if normalize:
            image = self.normalize(image)

        # 转换为张量
        if to_tensor:
            image = self.to_tensor(image)

        return image

    def augment(
        self,
        image: np.ndarray,
        augmentations: Optional[List[str]] = None,
    ) -> np.ndarray:
        """
        图像增强

        Args:
            image: 输入图像
            augmentations: 增强方法列表

        Returns:
            增强后的图像
        """
        if augmentations is None:
            augmentations = []

        for aug in augmentations:
            if aug == "flip_horizontal":
                image = cv2.flip(image, 1)
            elif aug == "flip_vertical":
                image = cv2.flip(image, 0)
            elif aug == "rotate_90":
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            elif aug == "rotate_180":
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif aug == "rotate_270":
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        return image
