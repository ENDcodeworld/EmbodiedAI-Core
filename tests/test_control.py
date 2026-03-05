"""
控制模块测试
"""

import pytest
import numpy as np
from embodiedai.control import RobotController, RobotConfig


class TestRobotConfig:
    """机器人配置测试"""

    def test_default_config(self):
        """测试默认配置"""
        config = RobotConfig()
        assert config.robot_type == "ur5e"
        assert config.dof == 6
        assert config.max_payload == 3.0
        assert config.reach == 0.8

    def test_custom_config(self):
        """测试自定义配置"""
        config = RobotConfig(robot_type="franka", dof=7, max_payload=5.0)
        assert config.robot_type == "franka"
        assert config.dof == 7
        assert config.max_payload == 5.0

    def test_to_dict(self):
        """测试转换为字典"""
        config = RobotConfig()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "robot_type" in config_dict
        assert "dof" in config_dict

    def test_from_dict(self):
        """测试从字典创建"""
        config_dict = {
            "robot_type": "ur10",
            "dof": 6,
            "max_payload": 10.0,
            "reach": 1.3,
        }
        config = RobotConfig.from_dict(config_dict)
        assert config.robot_type == "ur10"
        assert config.max_payload == 10.0


class TestRobotController:
    """机器人控制器测试"""

    def setup_method(self):
        """测试前设置"""
        self.config = RobotConfig()
        self.controller = RobotController(self.config)

    def test_initialization(self):
        """测试初始化"""
        assert self.controller.config == self.config
        assert self.controller.is_connected is False

    def test_connect_disconnect(self):
        """测试连接和断开"""
        assert self.controller.connect() is True
        assert self.controller.is_connected is True

        self.controller.disconnect()
        assert self.controller.is_connected is False

    def test_move_to(self):
        """测试移动到目标位置"""
        self.controller.connect()
        target = [0.5, 0.3, 0.2]
        assert self.controller.move_to(target) is True

        position = self.controller.get_position()
        assert np.allclose(position, target)

    def test_get_pose(self):
        """测试获取位姿"""
        position, orientation = self.controller.get_pose()
        assert position.shape == (3,)
        assert orientation.shape == (3,)

    def test_move_joints(self):
        """测试关节运动"""
        self.controller.connect()
        angles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        assert self.controller.move_joints(angles) is True

        joints = self.controller.get_joint_positions()
        assert np.allclose(joints, angles)

    def test_gripper_operations(self):
        """测试夹爪操作"""
        self.controller.connect()
        assert self.controller.gripper_open() is True
        assert self.controller.gripper_close(force=15.0) is True

    def test_emergency_stop(self):
        """测试紧急停止"""
        self.controller.connect()
        self.controller.emergency_stop()
        assert self.controller.is_connected is False

    def test_context_manager(self):
        """测试上下文管理器"""
        with RobotController() as controller:
            assert controller.is_connected is True
        assert controller.is_connected is False
