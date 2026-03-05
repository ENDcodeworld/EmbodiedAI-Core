"""
机器人配置模块
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class RobotConfig:
    """
    机器人配置类

    存储机器人的基本配置参数。

    Attributes:
        robot_type: 机器人类型
        dof: 自由度数量
        max_payload: 最大负载 (kg)
        reach: 工作范围 (m)
        joint_limits: 关节限位
        tcp_config: 工具中心点配置
    """

    robot_type: str = "ur5e"
    dof: int = 6
    max_payload: float = 3.0
    reach: float = 0.8
    joint_limits: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    tcp_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """初始化后处理"""
        if not self.joint_limits:
            self.joint_limits = self._get_default_joint_limits()

    def _get_default_joint_limits(self) -> Dict[str, Tuple[float, float]]:
        """获取默认关节限位"""
        # UR5e 默认关节限位 (弧度)
        limits = {
            "shoulder_pan": (-3.14, 3.14),
            "shoulder_lift": (-3.14, 3.14),
            "elbow": (-3.14, 3.14),
            "wrist_1": (-3.14, 3.14),
            "wrist_2": (-3.14, 3.14),
            "wrist_3": (-3.14, 3.14),
        }
        return limits

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "RobotConfig":
        """从字典创建配置"""
        return cls(**config_dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "robot_type": self.robot_type,
            "dof": self.dof,
            "max_payload": self.max_payload,
            "reach": self.reach,
            "joint_limits": self.joint_limits,
            "tcp_config": self.tcp_config,
        }
