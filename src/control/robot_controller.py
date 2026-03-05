"""
机器人控制器模块
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
from embodiedai.control.robot_config import RobotConfig


class RobotController:
    """
    机器人控制器

    提供机器人运动控制的基础接口。

    Attributes:
        config: 机器人配置
        is_connected: 是否已连接
        current_position: 当前位置
        current_orientation: 当前姿态
    """

    def __init__(self, config: Optional[RobotConfig] = None) -> None:
        """
        初始化机器人控制器

        Args:
            config: 机器人配置
        """
        self.config = config or RobotConfig()
        self.is_connected = False
        self._current_position = np.zeros(3)
        self._current_orientation = np.zeros(3)
        self._joint_positions = np.zeros(self.config.dof)

    def connect(self, host: str = "localhost", port: int = 30003) -> bool:
        """
        连接到机器人

        Args:
            host: 机器人 IP 地址
            port: 通信端口

        Returns:
            连接是否成功
        """
        # 模拟连接
        print(f"正在连接到机器人 {host}:{port}...")
        self.is_connected = True
        print("连接成功")
        return True

    def disconnect(self) -> None:
        """断开连接"""
        self.is_connected = False
        print("已断开连接")

    def move_to(
        self,
        position: Union[List[float], np.ndarray],
        orientation: Optional[Union[List[float], np.ndarray]] = None,
        velocity: float = 0.5,
        acceleration: float = 0.5,
    ) -> bool:
        """
        移动到目标位置

        Args:
            position: 目标位置 [x, y, z]
            orientation: 目标姿态 [rx, ry, rz]
            velocity: 速度 (m/s)
            acceleration: 加速度 (m/s²)

        Returns:
            移动是否成功
        """
        if not self.is_connected:
            print("错误：未连接到机器人")
            return False

        position = np.array(position)
        if len(position) != 3:
            print("错误：位置必须是 3 维向量")
            return False

        print(f"移动到位置：{position}")
        self._current_position = position

        if orientation is not None:
            self._current_orientation = np.array(orientation)

        return True

    def get_position(self) -> np.ndarray:
        """获取当前位置"""
        return self._current_position.copy()

    def get_orientation(self) -> np.ndarray:
        """获取当前姿态"""
        return self._current_orientation.copy()

    def get_pose(self) -> Tuple[np.ndarray, np.ndarray]:
        """获取当前位姿"""
        return self._current_position.copy(), self._current_orientation.copy()

    def move_joints(
        self,
        joint_angles: Union[List[float], np.ndarray],
        velocity: float = 0.5,
    ) -> bool:
        """
        关节运动

        Args:
            joint_angles: 目标关节角度
            velocity: 速度

        Returns:
            移动是否成功
        """
        if not self.is_connected:
            return False

        joint_angles = np.array(joint_angles)
        if len(joint_angles) != self.config.dof:
            print(f"错误：需要 {self.config.dof} 个关节角度")
            return False

        self._joint_positions = joint_angles
        print(f"关节运动：{joint_angles}")
        return True

    def get_joint_positions(self) -> np.ndarray:
        """获取当前关节位置"""
        return self._joint_positions.copy()

    def gripper_open(self) -> bool:
        """打开夹爪"""
        print("打开夹爪")
        return True

    def gripper_close(self, force: float = 10.0) -> bool:
        """
        关闭夹爪

        Args:
            force: 夹持力 (N)

        Returns:
            操作是否成功
        """
        print(f"关闭夹爪，力：{force}N")
        return True

    def emergency_stop(self) -> None:
        """紧急停止"""
        print("⚠️ 紧急停止!")
        self.is_connected = False

    def __enter__(self) -> "RobotController":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()
