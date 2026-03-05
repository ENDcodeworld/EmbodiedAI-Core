"""
轨迹生成器模块
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np


class TrajectoryGenerator:
    """
    轨迹生成器

    生成平滑的机器人运动轨迹。

    Attributes:
        time_step: 时间步长 (秒)
        max_velocity: 最大速度
        max_acceleration: 最大加速度
    """

    def __init__(
        self,
        time_step: float = 0.01,
        max_velocity: float = 1.0,
        max_acceleration: float = 2.0,
    ) -> None:
        """
        初始化轨迹生成器

        Args:
            time_step: 时间步长
            max_velocity: 最大速度
            max_acceleration: 最大加速度
        """
        self.time_step = time_step
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration

    def generate_linear_trajectory(
        self,
        start: Union[List[float], np.ndarray],
        goal: Union[List[float], np.ndarray],
        duration: float = 1.0,
    ) -> Dict[str, np.ndarray]:
        """
        生成线性轨迹

        Args:
            start: 起始位置
            goal: 目标位置
            duration: 运动时间 (秒)

        Returns:
            轨迹字典 {positions, velocities, accelerations, times}
        """
        start = np.array(start)
        goal = np.array(goal)

        n_steps = int(duration / self.time_step)
        times = np.linspace(0, duration, n_steps)

        # 线性插值
        positions = np.zeros((n_steps, len(start)))
        velocities = np.zeros((n_steps, len(start)))

        for i, t in enumerate(times):
            progress = t / duration
            positions[i] = start + progress * (goal - start)
            if i < n_steps - 1:
                velocities[i] = (goal - start) / duration

        return {
            "positions": positions,
            "velocities": velocities,
            "accelerations": np.zeros_like(velocities),
            "times": times,
        }

    def generate_joint_trajectory(
        self,
        start_angles: Union[List[float], np.ndarray],
        goal_angles: Union[List[float], np.ndarray],
        duration: float = 1.0,
    ) -> Dict[str, np.ndarray]:
        """
        生成关节空间轨迹

        Args:
            start_angles: 起始关节角度
            goal_angles: 目标关节角度
            duration: 运动时间

        Returns:
            轨迹字典
        """
        return self.generate_linear_trajectory(start_angles, goal_angles, duration)

    def generate_cubic_trajectory(
        self,
        start: Union[List[float], np.ndarray],
        goal: Union[List[float], np.ndarray],
        start_vel: float = 0.0,
        goal_vel: float = 0.0,
        duration: float = 1.0,
    ) -> Dict[str, np.ndarray]:
        """
        生成三次多项式轨迹

        Args:
            start: 起始位置
            goal: 目标位置
            start_vel: 起始速度
            goal_vel: 目标速度
            duration: 运动时间

        Returns:
            轨迹字典
        """
        start = np.array(start)
        goal = np.array(goal)

        n_steps = int(duration / self.time_step)
        times = np.linspace(0, duration, n_steps)

        # 三次多项式系数
        a0 = start
        a1 = start_vel
        a2 = 3 * (goal - start) / duration**2 - 2 * start_vel / duration - goal_vel / duration
        a3 = -2 * (goal - start) / duration**3 + (start_vel + goal_vel) / duration**2

        positions = np.zeros((n_steps, len(start)))
        velocities = np.zeros((n_steps, len(start)))
        accelerations = np.zeros((n_steps, len(start)))

        for i, t in enumerate(times):
            positions[i] = a0 + a1 * t + a2 * t**2 + a3 * t**3
            velocities[i] = a1 + 2 * a2 * t + 3 * a3 * t**2
            accelerations[i] = 2 * a2 + 6 * a3 * t

        return {
            "positions": positions,
            "velocities": velocities,
            "accelerations": accelerations,
            "times": times,
        }

    def smooth_trajectory(
        self,
        trajectory: Dict[str, np.ndarray],
        smoothing_factor: float = 0.1,
    ) -> Dict[str, np.ndarray]:
        """
        平滑轨迹

        Args:
            trajectory: 原始轨迹
            smoothing_factor: 平滑因子

        Returns:
            平滑后的轨迹
        """
        positions = trajectory["positions"].copy()

        # 简单移动平均平滑
        window = max(3, int(1 / smoothing_factor))
        for i in range(window // 2, len(positions) - window // 2):
            positions[i] = np.mean(positions[i - window // 2 : i + window // 2 + 1], axis=0)

        trajectory["positions"] = positions
        return trajectory
