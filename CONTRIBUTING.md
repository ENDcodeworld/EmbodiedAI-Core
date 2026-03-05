# 贡献指南 | Contributing to EmbodiedAI-Core

首先，感谢你考虑为 EmbodiedAI-Core 做出贡献！🎉

本指南将帮助你开始为项目做贡献。请花几分钟阅读以下内容。

## 📋 目录

- [行为准则](#行为准则)
- [我能如何贡献？](#我能如何贡献)
- [开发环境设置](#开发环境设置)
- [提交代码流程](#提交代码流程)
- [代码风格](#代码风格)
- [测试](#测试)
- [提交信息规范](#提交信息规范)
- [常见问题](#常见问题)

---

## 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

简而言之：
- 保持开放和包容
- 尊重不同观点
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---

## 我能如何贡献？

### 🐛 报告 Bug

发现 Bug？请创建 Issue 并提供：
- 清晰的标题和描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（OS、Python 版本等）
- 相关日志或截图

### 💡 提出功能建议

有好想法？欢迎提交 Feature Request：
- 描述功能和使用场景
- 说明为什么需要这个功能
- 如果可能，提供实现建议

### 📝 改进文档

文档同样重要！你可以帮助：
- 修正拼写和语法错误
- 补充缺失的说明
- 添加示例代码
- 翻译文档

### 🔧 提交代码

准备好贡献代码？请遵循以下流程。

---

## 开发环境设置

### 前置要求

- Python 3.11+
- Git
- CMake 3.20+ (用于编译 C++ 扩展)
- (可选) CUDA 11.8+ for GPU 加速

### 安装步骤

```bash
# 1. Fork 项目
# 在 GitHub 上点击 Fork 按钮

# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/EmbodiedAI-Core.git
cd EmbodiedAI-Core

# 3. 添加上游远程仓库
git remote add upstream https://github.com/ENDcodeworld/EmbodiedAI-Core.git

# 4. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 5. 安装开发依赖
pip install -e ".[dev]"

# 6. 验证安装
python -c "import embodiedai; print(embodiedai.__version__)"
```

---

## 提交代码流程

### 1. 创建分支

```bash
# 确保基于最新的主分支
git checkout main
git pull upstream main

# 创建功能分支
git checkout -b feature/amazing-feature
# 或修复分支
git checkout -b fix/bug-description
```

### 2. 进行更改

- 保持代码整洁
- 添加必要的注释
- 更新相关文档
- 编写测试用例

### 3. 运行测试

```bash
# 运行单元测试
pytest tests/

# 运行代码检查
flake8 src/
black --check src/
mypy src/
```

### 4. 提交更改

```bash
# 添加更改的文件
git add .

# 提交（遵循提交信息规范）
git commit -m "feat: add amazing feature"
```

### 5. 推送到 GitHub

```bash
git push origin feature/amazing-feature
```

### 6. 创建 Pull Request

1. 访问你的 Fork 页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述
4. 等待 CI 检查通过
5. 等待维护者审核

---

## 代码风格

### Python 代码

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用 [Black](https://black.readthedocs.io/) 格式化代码
- 使用 [isort](https://pycqa.github.io/isort/) 排序导入
- 使用 [flake8](https://flake8.pycqa.org/) 进行代码检查
- 使用类型注解 (Type Hints)

```python
# ✅ 好的示例
from typing import List, Optional

def process_data(
    data: List[float],
    threshold: Optional[float] = None
) -> List[float]:
    """处理数据并返回结果。
    
    Args:
        data: 输入数据列表
        threshold: 可选的阈值参数
        
    Returns:
        处理后的数据列表
    """
    if threshold is None:
        threshold = 0.5
    return [x for x in data if x > threshold]
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def function_name(param1: str, param2: int) -> bool:
    """简短的描述。
    
    更详细的描述（如果需要）。
    
    Args:
        param1: 参数 1 的描述
        param2: 参数 2 的描述
        
    Returns:
        返回值的描述
        
    Raises:
        ValueError: 当参数不正确时
    """
```

---

## 测试

### 编写测试

- 使用 pytest 框架
- 测试文件放在 `tests/` 目录
- 测试函数以 `test_` 开头
- 保持测试独立和可重复

```python
# tests/test_robot.py
import pytest
from embodiedai import Robot

def test_robot_initialization():
    """测试机器人初始化"""
    robot = Robot(config="test_config.yaml")
    assert robot is not None
    assert robot.is_connected() is False

def test_robot_movement():
    """测试机器人运动"""
    robot = Robot()
    robot.connect()
    robot.move_to([0.5, 0.3, 0.2])
    position = robot.get_position()
    assert len(position) == 3
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_robot.py

# 带覆盖率报告
pytest --cov=embodiedai --cov-report=html
```

---

## 提交信息规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (Type)

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 代码重构（非新功能，非 Bug 修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 示例

```bash
feat(vision): add YOLO-v8 support for object detection

- Integrate YOLO-v8 model
- Add configuration options
- Update documentation

Closes #123
```

```bash
fix(control): resolve connection timeout issue

- Increase default timeout from 5s to 10s
- Add retry logic for transient failures

Fixes #456
```

---

## 常见问题

### Q: 我的 PR 多久会被审核？

A: 我们会尽力在 48 小时内审核。如果超过一周没有回应，可以 @ 维护者。

### Q: 我可以一次提交多个功能吗？

A: 建议一个 PR 只做一件事。多个功能请分成多个 PR。

### Q: 我的代码没有通过 CI 检查怎么办？

A: 查看 CI 日志，修复问题后重新推送。CI 会自动重新运行。

### Q: 如何联系维护者？

A: 可以通过 Issue、Discord 或邮件联系我们。

---

## 🎉 感谢你的贡献！

每一个贡献，无论大小，都让 EmbodiedAI-Core 变得更好。

如果你有任何问题，欢迎随时提出！

---

**Happy Coding!** 🚀
