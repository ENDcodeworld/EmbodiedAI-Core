# 🤖 EmbodiedAI-Core

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Stars](https://img.shields.io/github/stars/ENDcodeworld/EmbodiedAI-Core.svg)](https://github.com/ENDcodeworld/EmbodiedAI-Core/stargazers)
[![Issues](https://img.shields.io/github/issues/ENDcodeworld/EmbodiedAI-Core.svg)](https://github.com/ENDcodeworld/EmbodiedAI-Core/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

<div align="center">

**🧠 具身智能核心框架 | Embodied AI Core Framework**

视觉 - 语言 - 动作模型 | 机器人控制 | 仿真环境 — 让具身智能开发更简单、更普惠

[🚀 快速开始](#-快速开始) · [📚 文档](#-文档) · [✨ 功能特性](#-功能特性) · [🤝 贡献指南](#-贡献指南) · [💬 社区](#-社区)

![EmbodiedAI Demo](./docs/assets/demo.png)
*图：EmbodiedAI-Core 机器人控制演示*

</div>

---

## 🌟 项目简介

EmbodiedAI-Core 是一个开源的具身智能（Embodied AI）核心框架，提供视觉 - 语言 - 动作（VLA）模型集成、机器人控制、仿真环境等功能，让具身智能开发更简单、更普惠。

### 核心价值

| 痛点 | EmbodiedAI-Core 解决方案 |
|------|------------------------|
| 🧠 VLA 模型集成复杂 | 开箱即用的模型集成接口 |
| 🦾 机器人控制门槛高 | 统一的机器人控制 API |
| 🎮 仿真环境配置繁琐 | 多仿真环境一键切换 |

---

## ✨ 功能特性

### 核心能力

| 功能 | 描述 | 状态 |
|------|------|------|
| 🧠 **VLA 模型** | 视觉 - 语言 - 动作模型集成 | 🚧 开发中 |
| 🦾 **机器人控制** | 机械臂/移动底盘控制接口 | 🚧 开发中 |
| 🎮 **仿真环境** | Isaac Sim/PyBullet/MuJoCo 支持 | 🚧 开发中 |
| 📊 **性能基准** | 标准化测试基准 | 📋 规划中 |
| 📚 **教程文档** | 从入门到进阶教程 | 📋 规划中 |

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- PyTorch 2.0+
- CUDA 11.7+ (GPU 加速，可选)

### 5 分钟快速体验

```bash
# 1. 克隆项目
git clone https://github.com/ENDcodeworld/EmbodiedAI-Core.git
cd EmbodiedAI-Core

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 3. 安装为可编辑模式
pip install -e ".[dev]"

# 4. 测试安装
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

## 📖 使用示例

### 视觉模块

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

### 机器人控制

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

### 运动规划

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

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **深度学习** | PyTorch 2.0+ | 核心 AI 框架 |
| **视觉处理** | OpenCV + torchvision | 图像处理 |
| **仿真环境** | Isaac Sim + PyBullet + MuJoCo | 多仿真支持 |
| **机器人** | ROS2 + MoveIt | 机器人操作系统 |
| **部署** | Docker + Kubernetes | 容器化编排 |

---

## 📚 文档

| 文档 | 说明 | 链接 |
|------|------|------|
| 📘 安装指南 | 详细安装步骤 | [查看](docs/installation.md) |
| 📗 快速入门 | 5 分钟上手教程 | [查看](docs/quickstart.md) |
| 📙 API 参考 | 完整 API 文档 | [查看](docs/api_reference.md) |
| 📕 示例代码 | 实用示例集合 | [查看](examples/) |
| 📒 贡献指南 | 如何贡献代码 | [查看](CONTRIBUTING.md) |

---

## 🗺️ 路线图

<div align="center">

| 时间 | 里程碑 | 状态 |
|------|--------|------|
| 2026 Q1 | 基础框架：核心模块实现 + 单元测试 | ✅ 已完成 |
| 2026 Q2 | 功能完善：多仿真支持 + VLA 模型集成 | 🚧 进行中 |
| 2026 Q3 | 生态建设：社区 + 插件系统 + 模型市场 | 📋 规划中 |
| 2026 Q4 | 生产就绪：性能优化 + 安全加固 | 📋 规划中 |

</div>

详细路线图请查看 [ROADMAP.md](docs/ROADMAP.md)

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 如何贡献

1. 🍴 **Fork 仓库** - 创建你自己的 fork
2. 🌿 **创建分支** - `git checkout -b feature/amazing-feature`
3. 💻 **开发** - 编写代码和测试
4. ✅ **测试** - 确保所有测试通过
5. 📤 **提交 PR** - 描述你的改动

### 开发环境设置

```bash
# Fork & Clone
git clone https://github.com/YOUR_USERNAME/EmbodiedAI-Core.git
cd EmbodiedAI-Core

# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v
```

### 代码规范

- **Python:** 遵循 PEP 8 + Black 格式化
- **提交信息:** 遵循 Conventional Commits 规范

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

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

---

## 📊 项目统计

[![Star History](https://api.star-history.com/svg?repos=ENDcodeworld/EmbodiedAI-Core&type=Date)](https://star-history.com/#ENDcodeworld/EmbodiedAI-Core&Date)

| 指标 | 数据 |
|------|------|
| ⭐ Stars | 0 |
| 🍴 Forks | 0 |
| 🐛 Issues | 0 |
| 📦 Downloads | 0 |

---

## 💬 社区

### 联系方式

| 平台 | 链接 |
|------|------|
| 🌐 官网 | https://embodiedai-core.com (即将上线) |
| 📧 邮箱 | contact@embodiedai-core.com |
| 💬 Discord | [加入社区](https://discord.gg/embodiedai) |
| 🐦 Twitter | [@EmbodiedAI_Core](https://twitter.com/EmbodiedAI_Core) |
| 📱 微信 | EmbodiedAI-Core 公众号 |
| 📺 B 站 | @EmbodiedAI-Core |

### 加入讨论

- 💬 **Discord 服务器**: [点击加入](https://discord.gg/embodiedai)
- 📱 **微信群**: 添加小助手微信 `embodiedai_helper` 邀请入群
- 🐦 **Twitter**: [@EmbodiedAI_Core](https://twitter.com/EmbodiedAI_Core)

---

## 💰 赞助商

EmbodiedAI-Core 是开源项目，感谢以下赞助商的支持：

<div align="center">

| 赞助商等级 | 赞助商 | 链接 |
|-----------|--------|------|
| 🏆 **金牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@embodiedai-core.com) |
| 🥈 **银牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@embodiedai-core.com) |
| 🥉 **铜牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@embodiedai-core.com) |

</div>

### 赞助方式

我们接受以下形式的赞助：

- 💰 **资金赞助** - 支持项目持续开发
- 🖥️ **云服务资源** - 服务器、存储、CDN
- 🎯 **推广支持** - 社交媒体分享、技术文章
- 👨‍💻 **人才赞助** - 开发者贡献时间

[👉 立即赞助](https://github.com/sponsors/EmbodiedAI-Core) | [📧 联系合作](mailto:sponsor@embodiedai-core.com)

---

## 🙏 致谢

感谢以下优秀的开源项目：

- [OpenVLA](https://github.com/openvla/openvla) - 开源 VLA 模型
- [RT-2](https://github.com/google-deepmind/rt-2) - Google 机器人模型
- [Isaac Sim](https://developer.nvidia.com/isaac/sim) - NVIDIA 仿真平台
- [ROS2](https://docs.ros.org/) - 机器人操作系统
- [PyTorch](https://pytorch.org/) - 深度学习框架

---

## 📄 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE) 文件

---

## 👥 团队

- **创始人**: 志哥
- **核心团队**: EmbodiedAI 开发团队
- **贡献者**: [查看贡献者列表](https://github.com/ENDcodeworld/EmbodiedAI-Core/graphs/contributors)

---

<div align="center">

### ⭐ 喜欢这个项目吗？

如果这个项目对你有帮助，请给我们一个 **Star** 支持！你的支持是我们持续开发的动力！

[![Star](https://img.shields.io/github/stars/ENDcodeworld/EmbodiedAI-Core?style=social)](https://github.com/ENDcodeworld/EmbodiedAI-Core)

---

**Made with ❤️ by AI 前沿社**

🤖 *让具身智能开发更简单*

[⬆ 返回顶部](#-embodiedai-core)

</div>

---

## 🔍 SEO 关键词

EmbodiedAI-Core, 具身智能，机器人控制，VLA 模型，视觉语言动作，仿真环境，open source, AI, machine learning, robotics, embodied AI, VLA
