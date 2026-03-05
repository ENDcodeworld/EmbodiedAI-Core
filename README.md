# 🤖 EmbodiedAI-Core

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Stars](https://img.shields.io/github/stars/ENDcodeworld/EmbodiedAI-Core.svg)](https://github.com/ENDcodeworld/EmbodiedAI-Core/stargazers)
[![Issues](https://img.shields.io/github/issues/ENDcodeworld/EmbodiedAI-Core.svg)](https://github.com/ENDcodeworld/EmbodiedAI-Core/issues)

<div align="center">

**具身智能核心框架 | Embodied AI Core Framework**

🧠 视觉 - 语言 - 动作模型 | 🦾 机器人控制 | 🎮 仿真环境

[文档](./docs/) · [示例](./examples/) · [论文](./docs/PAPERS.md)

</div>

---

## 🎯 项目概述

EmbodiedAI-Core 是一个开源的具身智能（Embodied AI）核心框架，提供视觉 - 语言 - 动作（VLA）模型集成、机器人控制、仿真环境等功能。

**愿景**：让具身智能开发更简单、更普惠。

---

## ✨ 核心特性

| 特性 | 说明 | 状态 |
|------|------|------|
| 🧠 **VLA 模型** | 视觉 - 语言 - 动作模型集成 | 🚧 开发中 |
| 🦾 **机器人控制** | 机械臂/移动底盘控制接口 | 🚧 开发中 |
| 🎮 **仿真环境** | Isaac Sim/PyBullet/MuJoCo 支持 | 🚧 开发中 |
| 📊 **性能基准** | 标准化测试基准 | 🚧 规划中 |
| 📚 **教程文档** | 从入门到进阶教程 | 🚧 规划中 |

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- PyTorch 2.0+
- CUDA 11.7+ (GPU 加速，可选)

### 安装

#### 使用 pip 安装（推荐）

```bash
pip install embodiedai-core
```

#### 从源码安装

```bash
# 克隆项目
git clone https://github.com/ENDcodeworld/EmbodiedAI-Core.git
cd EmbodiedAI-Core

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 安装为可编辑模式
pip install -e ".[dev]"

# 测试安装
python -c "import embodiedai; print(embodiedai.__version__)"
```

### 快速测试

```python
from embodiedai.vision import ImageProcessor
from embodiedai.control import RobotController
from embodiedai.motion import MotionPlanner
import numpy as np

# 视觉模块测试
processor = ImageProcessor()
image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
processed = processor.preprocess(image, resize_to=(224, 224))
print(f"✓ 视觉模块正常，输出形状：{processed.shape}")

# 控制模块测试
with RobotController() as controller:
    controller.move_to([0.5, 0.3, 0.2])
    print(f"✓ 控制模块正常，位置：{controller.get_position()}")

# 运动规划测试
planner = MotionPlanner()
planner.initialize()
path = planner.plan_path([0, 0, 0], [1, 1, 1])
print(f"✓ 运动规划正常，路径点数：{len(path)}")
```

---

## 📋 核心模块

### 1. 视觉模块

```python
from embodiedai.vision import VisionSystem, ImageProcessor
import numpy as np

# 图像处理器
processor = ImageProcessor(default_size=(224, 224))

# 创建测试图像
image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# 预处理
processed = processor.preprocess(image, normalize=True, to_tensor=True)

print(f"输入形状：{image.shape}")
print(f"输出形状：{processed.shape}")
# 输出：(480, 640, 3) -> (3, 224, 224)
```

### 2. 机器人控制

```python
from embodiedai.control import RobotController, RobotConfig

# 创建配置
config = RobotConfig(robot_type="ur5e")

# 创建控制器
with RobotController(config) as controller:
    controller.connect(host="192.168.1.100")
    
    # 笛卡尔空间运动
    controller.move_to([0.5, 0.3, 0.2])
    
    # 关节空间运动
    controller.move_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    
    # 夹爪控制
    controller.gripper_open()
    controller.gripper_close(force=10.0)
```

### 3. 运动规划

```python
from embodiedai.motion import MotionPlanner, TrajectoryGenerator

# 路径规划
planner = MotionPlanner()
planner.initialize()

start = [0.0, 0.0, 0.5]
goal = [0.5, 0.5, 0.5]
path = planner.plan_path(start, goal)

# 轨迹生成
generator = TrajectoryGenerator(time_step=0.01)
trajectory = generator.generate_linear_trajectory(start, goal, duration=1.0)

print(f"路径点数：{len(path)}")
print(f"轨迹点数：{len(trajectory['positions'])}")
```

---

## 📊 性能基准

### 任务成功率对比

| 任务 | OpenVLA | RT-2 | EmbodiedAI (目标) |
|------|---------|------|------------------|
| 物体抓取 | 85% | 82% | 90% |
| 物体放置 | 80% | 78% | 88% |
| 多步操作 | 65% | 60% | 75% |
| 泛化能力 | 70% | 68% | 80% |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                  EmbodiedAI-Core 架构                       │
├─────────────────────────────────────────────────────────────┤
│  感知层  →  决策层  →  控制层  →  执行层                   │
│    ↓          ↓          ↓          ↓                      │
│  视觉处理   VLA 模型   运动规划   机器人控制              │
│  语言理解   任务分解   轨迹生成   执行监控              │
└─────────────────────────────────────────────────────────────┘
```

**技术栈**:
- 深度学习：PyTorch 2.0+
- 视觉处理：OpenCV, torchvision
- 仿真环境：Isaac Sim, PyBullet, MuJoCo
- 机器人：ROS2, MoveIt

---

## 📖 文档

| 文档 | 说明 | 链接 |
|------|------|------|
| 安装指南 | 详细安装步骤 | [查看](docs/installation.md) |
| 快速入门 | 5 分钟上手教程 | [查看](docs/quickstart.md) |
| API 参考 | 完整 API 文档 | [查看](docs/api_reference.md) |
| 示例代码 | 实用示例集合 | [查看](examples/) |
| 贡献指南 | 如何贡献代码 | [查看](CONTRIBUTING.md) |

---

## 🤝 贡献指南

欢迎贡献代码、文档或建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_vision.py -v
pytest tests/test_control.py -v
pytest tests/test_motion.py -v

# 带覆盖率报告
pytest --cov=embodiedai --cov-report=html
```

## 📅 开发路线图

### Phase 1 (2026 Q1): 基础框架 ✅
- [x] 项目框架搭建
- [x] 核心模块实现 (vision, control, motion)
- [x] 单元测试
- [x] 文档完善
- [x] CI/CD 配置
- [ ] VLA 模型集成

### Phase 2 (2026 Q2): 功能完善
- [ ] 多仿真环境支持 (Isaac Sim, PyBullet, MuJoCo)
- [ ] VLA 模型集成 (OpenVLA, RT-2)
- [ ] 性能优化
- [ ] 更多示例代码
- [ ] 教程文档

### Phase 3 (2026 Q3): 生态建设
- [ ] 社区建设
- [ ] 插件系统
- [ ] 模型市场
- [ ] 开发者工具

---

## 📝 更新日志

### v0.1.0 (2026-03-05)
- 🎉 项目初始化
- ✅ 基础框架搭建
- ✅ 文档结构完善

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件

---

## 🙏 致谢

感谢以下开源项目：
- [OpenVLA](https://github.com/openvla/openvla)
- [RT-2](https://github.com/google-deepmind/rt-2)
- [Isaac Sim](https://developer.nvidia.com/isaac/sim)
- [ROS2](https://docs.ros.org/)

---

<div align="center">

**让具身智能开发更简单** 🤖

Made with ❤️ by AI 前沿社

</div>
