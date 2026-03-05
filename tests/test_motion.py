"""
运动规划模块测试
"""

import pytest
import numpy as np
from embodiedai.motion import MotionPlanner, TrajectoryGenerator


class TestMotionPlanner:
    """运动规划器测试"""

    def setup_method(self):
        """测试前设置"""
        self.planner = MotionPlanner(
            planning_time_limit=5.0,
            max_planning_iterations=1000,
        )

    def test_initialization(self):
        """测试初始化"""
        assert self.planner.planning_time_limit == 5.0
        assert self.planner.max_planning_iterations == 1000
        assert self.planner._is_initialized is False

    def test_initialize(self):
        """测试初始化规划器"""
        assert self.planner.initialize() is True
        assert self.planner._is_initialized is True

    def test_plan_path(self):
        """测试路径规划"""
        self.planner.initialize()
        start = [0.0, 0.0, 0.0]
        goal = [1.0, 1.0, 1.0]

        path = self.planner.plan_path(start, goal)
        assert path is not None
        assert len(path) > 0
        assert np.allclose(path[0], start)
        assert np.allclose(path[-1], goal)

    def test_plan_path_not_initialized(self):
        """测试未初始化时规划路径"""
        start = [0.0, 0.0, 0.0]
        goal = [1.0, 1.0, 1.0]

        path = self.planner.plan_path(start, goal)
        assert path is None

    def test_check_collision(self):
        """测试碰撞检测"""
        self.planner.initialize()
        config = [0.0] * 6
        assert self.planner.check_collision(config) is False

    def test_get_planning_info(self):
        """测试获取规划器信息"""
        info = self.planner.get_planning_info()
        assert isinstance(info, dict)
        assert "initialized" in info
        assert "time_limit" in info
        assert "max_iterations" in info


class TestTrajectoryGenerator:
    """轨迹生成器测试"""

    def setup_method(self):
        """测试前设置"""
        self.generator = TrajectoryGenerator(
            time_step=0.01,
            max_velocity=1.0,
            max_acceleration=2.0,
        )

    def test_initialization(self):
        """测试初始化"""
        assert self.generator.time_step == 0.01
        assert self.generator.max_velocity == 1.0
        assert self.generator.max_acceleration == 2.0

    def test_generate_linear_trajectory(self):
        """测试线性轨迹生成"""
        start = [0.0, 0.0, 0.0]
        goal = [1.0, 1.0, 1.0]
        duration = 1.0

        trajectory = self.generator.generate_linear_trajectory(start, goal, duration)

        assert "positions" in trajectory
        assert "velocities" in trajectory
        assert "accelerations" in trajectory
        assert "times" in trajectory

        assert trajectory["positions"].shape[0] == 100  # 1.0s / 0.01s
        assert trajectory["positions"].shape[1] == 3

    def test_generate_joint_trajectory(self):
        """测试关节轨迹生成"""
        start = [0.0] * 6
        goal = [0.5] * 6
        duration = 2.0

        trajectory = self.generator.generate_joint_trajectory(start, goal, duration)
        assert trajectory["positions"].shape[0] == 200  # 2.0s / 0.01s
        assert trajectory["positions"].shape[1] == 6

    def test_generate_cubic_trajectory(self):
        """测试三次多项式轨迹生成"""
        start = [0.0, 0.0, 0.0]
        goal = [1.0, 1.0, 1.0]
        duration = 1.0

        trajectory = self.generator.generate_cubic_trajectory(
            start, goal, start_vel=0.0, goal_vel=0.0, duration=duration
        )

        assert trajectory["positions"].shape[0] == 100
        assert trajectory["velocities"].shape[0] == 100
        assert trajectory["accelerations"].shape[0] == 100

    def test_smooth_trajectory(self):
        """测试轨迹平滑"""
        start = [0.0, 0.0, 0.0]
        goal = [1.0, 1.0, 1.0]

        trajectory = self.generator.generate_linear_trajectory(start, goal, 1.0)
        smoothed = self.generator.smooth_trajectory(trajectory, smoothing_factor=0.1)

        assert smoothed["positions"].shape == trajectory["positions"].shape
