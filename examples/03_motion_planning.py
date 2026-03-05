#!/usr/bin/env python3
"""
运动规划示例

演示如何使用运动规划器和轨迹生成器。
"""

import numpy as np
from embodiedai.motion import MotionPlanner, TrajectoryGenerator


def example_motion_planner():
    """运动规划器基础使用"""
    print("=" * 50)
    print("运动规划器示例")
    print("=" * 50)

    # 创建规划器
    planner = MotionPlanner(
        planning_time_limit=5.0,
        max_planning_iterations=1000,
    )

    # 初始化
    planner.initialize()

    # 规划路径
    start = [0.0, 0.0, 0.5]
    goal = [0.5, 0.5, 0.5]

    print(f"\n规划路径：{start} -> {goal}")
    path = planner.plan_path(start, goal)

    if path:
        print(f"路径点数：{len(path)}")
        print("路径点:")
        for i, waypoint in enumerate(path[::2]):  # 每隔一个显示
            print(f"  {i}: {waypoint}")

    # 获取规划器信息
    info = planner.get_planning_info()
    print(f"\n规划器状态：{info}")


def example_trajectory_generator():
    """轨迹生成器使用"""
    print("\n" + "=" * 50)
    print("轨迹生成器示例")
    print("=" * 50)

    # 创建轨迹生成器
    generator = TrajectoryGenerator(
        time_step=0.01,
        max_velocity=1.0,
        max_acceleration=2.0,
    )

    # 生成线性轨迹
    start = [0.0, 0.0, 0.0]
    goal = [1.0, 1.0, 1.0]
    duration = 2.0

    print(f"\n生成线性轨迹：{start} -> {goal}, 时间：{duration}s")
    trajectory = generator.generate_linear_trajectory(start, goal, duration)

    print(f"轨迹点数：{len(trajectory['positions'])}")
    print(f"时间范围：[{trajectory['times'][0]:.2f}, {trajectory['times'][-1]:.2f}]s")
    print(f"位置范围：[{trajectory['positions'][0]}, {trajectory['positions'][-1]}]")

    # 生成关节轨迹
    print("\n生成关节轨迹:")
    joint_start = [0.0] * 6
    joint_goal = [0.5, 0.3, 0.4, 0.2, 0.1, 0.6]

    joint_trajectory = generator.generate_joint_trajectory(
        joint_start, joint_goal, duration=1.5
    )
    print(f"关节轨迹点数：{len(joint_trajectory['positions'])}")


def example_cubic_trajectory():
    """三次多项式轨迹"""
    print("\n" + "=" * 50)
    print("三次多项式轨迹示例")
    print("=" * 50)

    generator = TrajectoryGenerator(time_step=0.01)

    start = [0.0, 0.0, 0.5]
    goal = [0.5, 0.5, 0.5]

    trajectory = generator.generate_cubic_trajectory(
        start, goal, start_vel=0.0, goal_vel=0.0, duration=1.0
    )

    print(f"起始速度：{trajectory['velocities'][0]}")
    print(f"结束速度：{trajectory['velocities'][-1]}")
    print(f"最大加速度：{np.max(np.abs(trajectory['accelerations'])):.3f}")


def example_trajectory_smoothing():
    """轨迹平滑示例"""
    print("\n" + "=" * 50)
    print("轨迹平滑示例")
    print("=" * 50)

    generator = TrajectoryGenerator(time_step=0.01)

    start = [0.0, 0.0, 0.0]
    goal = [1.0, 1.0, 1.0]

    # 生成原始轨迹
    trajectory = generator.generate_linear_trajectory(start, goal, 1.0)

    # 平滑轨迹
    smoothed = generator.smooth_trajectory(trajectory, smoothing_factor=0.1)

    print("轨迹平滑完成")
    print(f"原始轨迹点数：{len(trajectory['positions'])}")
    print(f"平滑后轨迹点数：{len(smoothed['positions'])}")


def example_complete_task():
    """完整任务示例：规划 + 执行"""
    print("\n" + "=" * 50)
    print("完整任务示例")
    print("=" * 50)

    # 初始化规划器和轨迹生成器
    planner = MotionPlanner()
    planner.initialize()

    generator = TrajectoryGenerator(time_step=0.01)

    # 规划路径
    start = [0.0, 0.0, 0.5]
    via_point = [0.3, 0.3, 0.5]
    goal = [0.5, 0.5, 0.5]

    path1 = planner.plan_path(start, via_point)
    path2 = planner.plan_path(via_point, goal)

    if path1 and path2:
        full_path = path1[:-1] + path2
        print(f"完整路径点数：{len(full_path)}")

        # 为每段路径生成轨迹
        for i in range(len(full_path) - 1):
            traj = generator.generate_linear_trajectory(
                full_path[i], full_path[i + 1], duration=0.5
            )
            # 这里可以发送给机器人执行

    print("✓ 任务规划完成!")


if __name__ == "__main__":
    example_motion_planner()
    example_trajectory_generator()
    example_cubic_trajectory()
    example_trajectory_smoothing()
    example_complete_task()

    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)
