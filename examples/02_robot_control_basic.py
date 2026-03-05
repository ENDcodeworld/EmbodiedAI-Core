#!/usr/bin/env python3
"""
机器人控制基础示例

演示如何使用机器人控制器进行基本运动控制。
"""

from embodiedai.control import RobotController, RobotConfig


def example_robot_config():
    """机器人配置示例"""
    print("=" * 50)
    print("机器人配置示例")
    print("=" * 50)

    # 默认配置 (UR5e)
    config = RobotConfig()
    print(f"机器人类型：{config.robot_type}")
    print(f"自由度：{config.dof}")
    print(f"最大负载：{config.max_payload} kg")
    print(f"工作范围：{config.reach} m")

    # 自定义配置
    custom_config = RobotConfig(
        robot_type="franka_emika",
        dof=7,
        max_payload=3.0,
        reach=0.8,
    )
    print(f"\n自定义配置：{custom_config.robot_type}")


def example_robot_controller():
    """机器人控制器基础使用"""
    print("\n" + "=" * 50)
    print("机器人控制器示例")
    print("=" * 50)

    # 创建控制器
    config = RobotConfig(robot_type="ur5e")
    controller = RobotController(config)

    # 连接机器人
    controller.connect(host="192.168.1.100", port=30003)

    # 笛卡尔空间运动
    print("\n笛卡尔空间运动:")
    controller.move_to([0.5, 0.3, 0.2], velocity=0.3)
    position = controller.get_position()
    print(f"当前位置：{position}")

    # 关节空间运动
    print("\n关节空间运动:")
    joint_angles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    controller.move_joints(joint_angles)
    joints = controller.get_joint_positions()
    print(f"当前关节角度：{joints}")

    # 夹爪操作
    print("\n夹爪操作:")
    controller.gripper_open()
    controller.gripper_close(force=10.0)

    # 断开连接
    controller.disconnect()


def example_context_manager():
    """使用上下文管理器"""
    print("\n" + "=" * 50)
    print("上下文管理器示例")
    print("=" * 50)

    with RobotController() as controller:
        print(f"连接状态：{controller.is_connected}")
        controller.move_to([0.4, 0.2, 0.3])
        print(f"位置：{controller.get_position()}")

    print(f"退出上下文后连接状态：{controller.is_connected}")


def example_pick_and_place():
    """模拟抓取 - 放置任务"""
    print("\n" + "=" * 50)
    print("抓取 - 放置任务示例")
    print("=" * 50)

    with RobotController() as controller:
        # 移动到预备位置
        print("1. 移动到预备位置")
        controller.move_to([0.5, 0.0, 0.3])

        # 下降到抓取位置
        print("2. 下降到抓取位置")
        controller.move_to([0.5, 0.0, 0.1])

        # 闭合夹爪
        print("3. 闭合夹爪")
        controller.gripper_close(force=15.0)

        # 抬起
        print("4. 抬起")
        controller.move_to([0.5, 0.0, 0.3])

        # 移动到放置位置
        print("5. 移动到放置位置")
        controller.move_to([0.3, 0.4, 0.3])

        # 下降到放置位置
        print("6. 下降到放置位置")
        controller.move_to([0.3, 0.4, 0.1])

        # 打开夹爪
        print("7. 打开夹爪")
        controller.gripper_open()

        # 抬起
        print("8. 抬起")
        controller.move_to([0.3, 0.4, 0.3])

        print("✓ 任务完成!")


if __name__ == "__main__":
    example_robot_config()
    example_robot_controller()
    example_context_manager()
    example_pick_and_place()

    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)
