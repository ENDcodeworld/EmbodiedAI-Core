"""
EmbodiedAI-Core - 具身智能核心框架

A core framework for Embodied AI, providing vision-language-action (VLA)
model integration, robot control, and simulation environments.

具身智能核心框架，提供视觉 - 语言 - 动作（VLA）模型集成、
机器人控制、仿真环境等功能。
"""

from embodiedai.vision import VisionSystem, ImageProcessor
from embodiedai.control import RobotController, RobotConfig
from embodiedai.motion import MotionPlanner, TrajectoryGenerator

__version__ = "0.1.0"
__author__ = "EmbodiedAI-Core Contributors"
__email__ = "embodiedai@example.com"
__all__ = [
    "VisionSystem",
    "ImageProcessor",
    "RobotController",
    "RobotConfig",
    "MotionPlanner",
    "TrajectoryGenerator",
]
