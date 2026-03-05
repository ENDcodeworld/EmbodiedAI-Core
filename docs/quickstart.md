# 快速入门 | Quick Start

5 分钟快速上手 EmbodiedAI-Core。

## 📋 目录

- [前置准备](#前置准备)
- [第一个程序](#第一个程序)
- [核心模块概览](#核心模块概览)
- [完整示例](#完整示例)
- [下一步](#下一步)

---

## 前置准备

确保已安装 EmbodiedAI-Core：

```bash
pip install embodiedai-core
```

验证安装：

```bash
python -c "import embodiedai; print(embodiedai.__version__)"
```

---

## 第一个程序

### 示例 1: 图像处理

```python
import numpy as np
from embodiedai.vision import ImageProcessor

# 创建图像处理器
processor = ImageProcessor(default_size=(224, 224))

# 创建测试图像
image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# 预处理
processed = processor.preprocess(image, normalize=True, to_tensor=True)

print(f"输入形状：{image.shape}")
print(f"输出形状：{processed.shape}")
# 输出：输入形状：(480, 640, 3)
#       输出形状：(3, 224, 224)
```

### 示例 2: 机器人控制

```python
from embodiedai.control import RobotController, RobotConfig

# 创建机器人配置
config = RobotConfig(robot_type="ur5e")

# 创建控制器
with RobotController(config) as controller:
    # 连接到机器人
    controller.connect(host="192.168.1.100")
    
    # 移动到目标位置
    controller.move_to([0.5, 0.3, 0.2])
    
    # 获取当前位置
    position = controller.get_position()
    print(f"当前位置：{position}")
    
    # 夹爪操作
    controller.gripper_open()
    controller.gripper_close(force=10.0)
```

### 示例 3: 运动规划

```python
from embodiedai.motion import MotionPlanner, TrajectoryGenerator

# 创建规划器
planner = MotionPlanner()
planner.initialize()

# 规划路径
start = [0.0, 0.0, 0.5]
goal = [0.5, 0.5, 0.5]
path = planner.plan_path(start, goal)

print(f"路径点数：{len(path)}")

# 生成轨迹
generator = TrajectoryGenerator(time_step=0.01)
trajectory = generator.generate_linear_trajectory(start, goal, duration=1.0)

print(f"轨迹点数：{len(trajectory['positions'])}")
```

---

## 核心模块概览

### 1. 视觉模块 (embodiedai.vision)

```python
from embodiedai.vision import VisionSystem, ImageProcessor

# 视觉系统 - 图像采集
with VisionSystem(camera_id=0) as vs:
    frame = vs.capture_frame()

# 图像处理器 - 预处理
processor = ImageProcessor()
processed = processor.preprocess(image, resize_to=(224, 224))
```

**主要功能**:
- 图像采集
- 图像预处理
- 图像增强
- 特征提取

### 2. 控制模块 (embodiedai.control)

```python
from embodiedai.control import RobotController, RobotConfig

# 配置
config = RobotConfig(robot_type="ur5e")

# 控制器
controller = RobotController(config)
controller.connect()
controller.move_to([x, y, z])
controller.gripper_close()
```

**主要功能**:
- 机器人连接
- 笛卡尔空间运动
- 关节空间运动
- 夹爪控制

### 3. 运动规划模块 (embodiedai.motion)

```python
from embodiedai.motion import MotionPlanner, TrajectoryGenerator

# 路径规划
planner = MotionPlanner()
path = planner.plan_path(start, goal)

# 轨迹生成
generator = TrajectoryGenerator()
trajectory = generator.generate_linear_trajectory(start, goal, 1.0)
```

**主要功能**:
- 路径规划
- 轨迹生成
- 碰撞检测
- 轨迹优化

---

## 完整示例

### 视觉伺服抓取任务

```python
"""
视觉伺服抓取示例

结合视觉、控制和运动规划完成抓取任务。
"""

import numpy as np
from embodiedai.vision import VisionSystem, ImageProcessor
from embodiedai.control import RobotController
from embodiedai.motion import MotionPlanner, TrajectoryGenerator


def detect_object(image):
    """模拟物体检测"""
    # 实际应用中这里会使用深度学习模型
    return {"position": [0.5, 0.3, 0.1], "confidence": 0.95}


def pick_and_place():
    """执行抓取 - 放置任务"""
    
    # 初始化模块
    with VisionSystem(camera_id=0) as vision:
        processor = ImageProcessor()
        
        controller = RobotController()
        controller.connect()
        
        planner = MotionPlanner()
        planner.initialize()
        generator = TrajectoryGenerator(time_step=0.01)
        
        # 1. 采集图像
        print("1. 采集图像...")
        image = vision.capture_frame()
        
        # 2. 预处理
        print("2. 图像预处理...")
        processed = processor.preprocess(image, resize_to=(224, 224))
        
        # 3. 检测物体
        print("3. 检测物体...")
        object_info = detect_object(processed)
        object_pos = object_info["position"]
        print(f"   物体位置：{object_pos}")
        
        # 4. 规划路径
        print("4. 规划路径...")
        home_pos = [0.5, 0.0, 0.3]
        path = planner.plan_path(home_pos, object_pos)
        
        # 5. 生成轨迹
        print("5. 生成轨迹...")
        trajectory = generator.generate_linear_trajectory(
            home_pos, object_pos, duration=1.0
        )
        
        # 6. 执行抓取
        print("6. 执行抓取...")
        controller.move_to([object_pos[0], object_pos[1], 0.2])  # 预备位置
        controller.move_to(object_pos)  # 抓取位置
        controller.gripper_close(force=15.0)  # 闭合夹爪
        
        # 7. 放置
        print("7. 放置物体...")
        place_pos = [0.3, 0.4, 0.1]
        controller.move_to([place_pos[0], place_pos[1], 0.2])
        controller.move_to(place_pos)
        controller.gripper_open()  # 打开夹爪
        
        # 8. 返回
        print("8. 返回初始位置...")
        controller.move_to(home_pos)
        
        print("✓ 任务完成!")


if __name__ == "__main__":
    pick_and_place()
```

---

## 下一步

现在你已经掌握了基础知识，可以进一步学习：

- [安装指南](./installation.md) - 详细安装步骤
- [API 参考](./api_reference.md) - 完整 API 文档
- [示例代码](../examples/) - 更多实用示例
- [贡献指南](../CONTRIBUTING.md) - 如何贡献代码

---

**有问题？** 查看 [GitHub Issues](https://github.com/ENDcodeworld/EmbodiedAI-Core/issues) 或加入我们的社区！
