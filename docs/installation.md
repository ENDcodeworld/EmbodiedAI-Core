# 安装指南 | Installation Guide

本指南将帮助你在不同环境下安装 EmbodiedAI-Core。

## 📋 目录

- [系统要求](#系统要求)
- [快速安装](#快速安装)
- [从源码安装](#从源码安装)
- [Docker 安装](#docker 安装)
- [开发环境设置](#开发环境设置)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

---

## 系统要求

### 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 4 核心 | 8 核心+ |
| RAM | 8 GB | 16 GB+ |
| GPU | 可选 | NVIDIA RTX 3060+ |
| 存储 | 10 GB | 50 GB+ SSD |

### 软件要求

- **操作系统**: Ubuntu 20.04+, macOS 12+, Windows 11
- **Python**: 3.11 或 3.12
- **CUDA**: 11.7+ (GPU 加速必需)
- **CMake**: 3.20+ (编译 C++ 扩展)

---

## 快速安装

### 使用 pip 安装（推荐）

```bash
# 安装稳定版
pip install embodiedai-core

# 安装最新版
pip install embodiedai-core --upgrade
```

### 安装可选依赖

```bash
# 开发依赖
pip install embodiedai-core[dev]

# 文档构建依赖
pip install embodiedai-core[docs]

# 仿真环境依赖
pip install embodiedai-core[simulation]

# 全部依赖
pip install embodiedai-core[dev,docs,simulation]
```

---

## 从源码安装

### 1. 克隆仓库

```bash
git clone https://github.com/ENDcodeworld/EmbodiedAI-Core.git
cd EmbodiedAI-Core
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 或使用 conda
conda create -n embodiedai python=3.11
conda activate embodiedai
```

### 3. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装为可编辑模式（开发推荐）
pip install -e ".[dev]"
```

### 4. 验证安装

```bash
python -c "import embodiedai; print(embodiedai.__version__)"
```

---

## Docker 安装

### 拉取镜像

```bash
# 生产镜像
docker pull embodiedai/core:latest

# 开发镜像
docker pull embodiedai/core:development
```

### 运行容器

```bash
# 基本运行
docker run -it embodiedai/core:latest

# 开发模式（挂载代码）
docker run -it -v $(pwd):/app embodiedai/core:development

# GPU 支持
docker run -it --gpus all embodiedai/core:latest
```

### 构建镜像

```bash
# 生产镜像
docker build -t embodiedai/core:latest --target production .

# 开发镜像
docker build -t embodiedai/core:dev --target development .
```

---

## 开发环境设置

### 1. 安装开发依赖

```bash
pip install -e ".[dev,docs]"
```

### 2. 配置 pre-commit

```bash
# 安装 pre-commit
pre-commit install

# 验证安装
pre-commit run --all-files
```

### 3. 配置 IDE

#### VS Code

安装以下扩展：
- Python (Microsoft)
- Pylance
- Black Formatter
- isort

创建 `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python"
}
```

#### PyCharm

1. 设置 Python 解释器为项目虚拟环境
2. 启用 Black 格式化
3. 配置 isort 导入排序

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_vision.py -v

# 带覆盖率报告
pytest --cov=embodiedai --cov-report=html
```

---

## 验证安装

### 基础验证

```python
import embodiedai

print(f"版本：{embodiedai.__version__}")
print(f"作者：{embodiedai.__author__}")
```

### 模块验证

```python
# 视觉模块
from embodiedai.vision import VisionSystem, ImageProcessor
print("✓ 视觉模块导入成功")

# 控制模块
from embodiedai.control import RobotController, RobotConfig
print("✓ 控制模块导入成功")

# 运动规划模块
from embodiedai.motion import MotionPlanner, TrajectoryGenerator
print("✓ 运动规划模块导入成功")
```

### 功能验证

```python
import numpy as np
from embodiedai.vision import ImageProcessor

# 测试图像处理
processor = ImageProcessor()
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
processed = processor.preprocess(test_image, resize_to=(224, 224))
print(f"✓ 图像处理成功，输出形状：{processed.shape}")
```

---

## 常见问题

### Q1: pip 安装失败

**问题**: `ERROR: Could not find a version that satisfies the requirement embodiedai-core`

**解决**:
```bash
# 升级 pip
pip install --upgrade pip

# 检查 Python 版本
python --version  # 需要 3.11+

# 使用国内镜像
pip install embodiedai-core -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: CUDA 相关错误

**问题**: `CUDA not available` 或 `libcudart.so not found`

**解决**:
```bash
# 检查 CUDA 安装
nvcc --version

# 重新安装 PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Q3: 编译错误

**问题**: 安装时出现 C++ 编译错误

**解决**:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake

# macOS
xcode-select --install

# Windows
# 安装 Visual Studio Build Tools
```

### Q4: 依赖冲突

**问题**: `ERROR: Cannot install ... these packages have conflicting dependencies`

**解决**:
```bash
# 创建新的虚拟环境
python -m venv venv
source venv/bin/activate

# 重新安装
pip install embodiedai-core
```

### Q5: 导入错误

**问题**: `ModuleNotFoundError: No module named 'embodiedai'`

**解决**:
```bash
# 确认虚拟环境已激活
which python  # Linux/macOS
where python  # Windows

# 重新安装
pip install -e .
```

---

## 下一步

安装完成后，请查看：

- [快速入门](./quickstart.md) - 5 分钟上手教程
- [API 参考](./api_reference.md) - 完整 API 文档
- [示例代码](../examples/) - 实用示例集合

---

**遇到问题？** 请查看 [GitHub Issues](https://github.com/ENDcodeworld/EmbodiedAI-Core/issues) 或提交新问题。
