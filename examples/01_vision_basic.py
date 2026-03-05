#!/usr/bin/env python3
"""
视觉模块基础示例

演示如何使用视觉系统进行图像采集和处理。
"""

import numpy as np
from embodiedai.vision import VisionSystem, ImageProcessor


def example_vision_system():
    """视觉系统基础使用示例"""
    print("=" * 50)
    print("视觉系统基础示例")
    print("=" * 50)

    # 创建视觉系统
    with VisionSystem(camera_id=0, resolution=(640, 480)) as vs:
        print(f"摄像头 ID: {vs.camera_id}")
        print(f"分辨率：{vs.resolution}")
        print(f"帧率：{vs.fps}")
        print(f"状态：{'活跃' if vs.is_active else '未激活'}")

        # 捕获图像（实际使用时取消注释）
        # frame = vs.capture_frame()
        # if frame is not None:
        #     print(f"捕获图像形状：{frame.shape}")


def example_image_processor():
    """图像处理器使用示例"""
    print("\n" + "=" * 50)
    print("图像处理器示例")
    print("=" * 50)

    # 创建图像处理器
    processor = ImageProcessor(default_size=(224, 224))

    # 创建测试图像
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    print(f"原始图像形状：{test_image.shape}")

    # 调整大小
    resized = processor.resize(test_image, (224, 224))
    print(f"调整后形状：{resized.shape}")

    # 归一化
    normalized = processor.normalize(test_image)
    print(f"归一化后范围：[{normalized.min():.3f}, {normalized.max():.3f}]")

    # 完整预处理
    processed = processor.preprocess(
        test_image,
        resize_to=(224, 224),
        normalize=True,
        to_tensor=True,
    )
    print(f"预处理后形状：{processed.shape}")

    # 图像增强
    augmented = processor.augment(test_image, ["flip_horizontal", "rotate_90"])
    print(f"增强后形状：{augmented.shape}")


def example_vla_input_preparation():
    """VLA 模型输入准备示例"""
    print("\n" + "=" * 50)
    print("VLA 模型输入准备")
    print("=" * 50)

    processor = ImageProcessor(default_size=(224, 224))

    # 模拟相机图像
    camera_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # 预处理为 VLA 模型输入
    vla_input = processor.preprocess(
        camera_image,
        resize_to=(224, 224),
        normalize=True,
        to_tensor=True,
    )

    print(f"VLA 输入形状：{vla_input.shape}")
    print(f"VLA 输入数据类型：{vla_input.dtype}")
    print("✓ 图像已准备好输入 VLA 模型")


if __name__ == "__main__":
    example_vision_system()
    example_image_processor()
    example_vla_input_preparation()

    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)
