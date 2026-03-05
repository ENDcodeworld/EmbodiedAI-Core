# API 参考 | API Reference

EmbodiedAI-Core 完整 API 文档。

## 📋 目录

- [视觉模块](#视觉模块)
- [控制模块](#控制模块)
- [运动规划模块](#运动规划模块)

---

## 视觉模块

### VisionSystem

视觉系统基类，提供图像采集功能。

#### 初始化

```python
VisionSystem(
    camera_id: int = 0,
    resolution: Tuple[int, int] = (640, 480),
    fps: int = 30
)
```

**参数**:
- `camera_id`: 摄像头设备 ID
- `resolution`: 图像分辨率 (宽，高)
- `fps`: 帧率

**示例**:
```python
vs = VisionSystem(camera_id=0, resolution=(640, 480))
vs.initialize()
```

#### 方法

##### initialize()

初始化摄像头。

**返回**: `bool` - 初始化是否成功

##### capture_frame()

捕获单帧图像 (BGR 格式)。

**返回**: `Optional[np.ndarray]` - 图像数组

##### capture_rgb()

捕获 RGB 图像。

**返回**: `Optional[np.ndarray]` - RGB 图像数组

##### shutdown()

关闭摄像头。

---

### ImageProcessor

图像处理器，提供图像预处理功能。

#### 初始化

```python
ImageProcessor(
    default_size: Optional[Tuple[int, int]] = (224, 224),
    normalization: bool = True
)
```

**参数**:
- `default_size`: 默认输出尺寸
- `normalization`: 是否进行归一化

#### 方法

##### resize()

```python
resize(
    image: Union[np.ndarray, Image.Image],
    size: Optional[Tuple[int, int]] = None
) -> np.ndarray
```

调整图像大小。

##### normalize()

```python
normalize(
    image: np.ndarray,
    mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
    std: Tuple[float, ...] = (0.229, 0.224, 0.225)
) -> np.ndarray
```

归一化图像。

##### to_tensor()

```python
to_tensor(
    image: np.ndarray,
    channel_first: bool = True
) -> np.ndarray
```

转换为张量格式。

##### preprocess()

```python
preprocess(
    image: Union[np.ndarray, Image.Image, str],
    resize_to: Optional[Tuple[int, int]] = None,
    normalize: bool = True,
    to_tensor: bool = True
) -> np.ndarray
```

完整的图像预处理流程。

**参数**:
- `image`: 输入图像 (数组、PIL Image 或文件路径)
- `resize_to`: 调整到的尺寸
- `normalize`: 是否归一化
- `to_tensor`: 是否转换为张量

**返回**: 预处理后的图像

**示例**:
```python
processor = ImageProcessor()
processed = processor.preprocess(
    "image.jpg",
    resize_to=(224, 224),
    normalize=True,
    to_tensor=True
)
```

##### augment()

```python
augment(
    image: np.ndarray,
    augmentations: Optional[List[str]] = None
) -> np.ndarray
```

图像增强。

**支持的增强**:
- `flip_horizontal`: 水平翻转
- `flip_vertical`: 垂直翻转
- `rotate_90`: 旋转 90 度
- `rotate_180`: 旋转 180 度
- `rotate_270`: 旋转 270 度

---

## 控制模块

### RobotConfig

机器人配置类。

#### 初始化

```python
RobotConfig(
    robot_type: str = "ur5e",
    dof: int = 6,
    max_payload: float = 3.0,
    reach: float = 0.8,
    joint_limits: Dict[str, Tuple[float, float]] = None,
    tcp_config: Dict[str, Any] = None
)
```

**参数**:
- `robot_type`: 机器人类型
- `dof`: 自由度数量
- `max_payload`: 最大负载 (kg)
- `reach`: 工作范围 (m)
- `joint_limits`: 关节限位
- `tcp_config`: 工具中心点配置

#### 方法

##### from_dict()

```python
@classmethod
from_dict(config_dict: Dict[str, Any]) -> RobotConfig
```

从字典创建配置。

##### to_dict()

```python
to_dict() -> Dict[str, Any]
```

转换为字典。

---

### RobotController

机器人控制器。

#### 初始化

```python
RobotController(config: Optional[RobotConfig] = None)
```

**参数**:
- `config`: 机器人配置

#### 方法

##### connect()

```python
connect(host: str = "localhost", port: int = 30003) -> bool
```

连接到机器人。

##### disconnect()

断开连接。

##### move_to()

```python
move_to(
    position: Union[List[float], np.ndarray],
    orientation: Optional[Union[List[float], np.ndarray]] = None,
    velocity: float = 0.5,
    acceleration: float = 0.5
) -> bool
```

移动到目标位置。

**参数**:
- `position`: 目标位置 [x, y, z]
- `orientation`: 目标姿态 [rx, ry, rz]
- `velocity`: 速度 (m/s)
- `acceleration`: 加速度 (m/s²)

##### move_joints()

```python
move_joints(
    joint_angles: Union[List[float], np.ndarray],
    velocity: float = 0.5
) -> bool
```

关节运动。

##### get_position()

```python
get_position() -> np.ndarray
```

获取当前位置。

##### get_orientation()

```python
get_orientation() -> np.ndarray
```

获取当前姿态。

##### get_pose()

```python
get_pose() -> Tuple[np.ndarray, np.ndarray]
```

获取当前位姿。

##### get_joint_positions()

```python
get_joint_positions() -> np.ndarray
```

获取当前关节位置。

##### gripper_open()

```python
gripper_open() -> bool
```

打开夹爪。

##### gripper_close()

```python
gripper_close(force: float = 10.0) -> bool
```

关闭夹爪。

**参数**:
- `force`: 夹持力 (N)

##### emergency_stop()

紧急停止。

---

## 运动规划模块

### MotionPlanner

运动规划器。

#### 初始化

```python
MotionPlanner(
    planning_time_limit: float = 5.0,
    max_planning_iterations: int = 1000
)
```

**参数**:
- `planning_time_limit`: 规划时间限制 (秒)
- `max_planning_iterations`: 最大迭代次数

#### 方法

##### initialize()

```python
initialize(
    robot_config: Optional[Dict[str, Any]] = None,
    environment: Optional[Dict[str, Any]] = None
) -> bool
```

初始化规划器。

##### plan_path()

```python
plan_path(
    start: Union[List[float], np.ndarray],
    goal: Union[List[float], np.ndarray],
    obstacles: Optional[List[Dict[str, Any]]] = None
) -> Optional[List[np.ndarray]]
```

规划路径。

**参数**:
- `start`: 起始位置
- `goal`: 目标位置
- `obstacles`: 障碍物列表

**返回**: 路径点列表，失败返回 None

##### plan_cartesian_path()

```python
plan_cartesian_path(
    waypoints: List[Union[List[float], np.ndarray]]
) -> Optional[List[np.ndarray]]
```

规划笛卡尔空间路径。

##### check_collision()

```python
check_collision(
    configuration: Union[List[float], np.ndarray],
    obstacles: Optional[List[Dict[str, Any]]] = None
) -> bool
```

碰撞检测。

**返回**: 是否发生碰撞

##### get_planning_info()

```python
get_planning_info() -> Dict[str, Any]
```

获取规划器信息。

---

### TrajectoryGenerator

轨迹生成器。

#### 初始化

```python
TrajectoryGenerator(
    time_step: float = 0.01,
    max_velocity: float = 1.0,
    max_acceleration: float = 2.0
)
```

**参数**:
- `time_step`: 时间步长 (秒)
- `max_velocity`: 最大速度
- `max_acceleration`: 最大加速度

#### 方法

##### generate_linear_trajectory()

```python
generate_linear_trajectory(
    start: Union[List[float], np.ndarray],
    goal: Union[List[float], np.ndarray],
    duration: float = 1.0
) -> Dict[str, np.ndarray]
```

生成线性轨迹。

**返回**: 轨迹字典 `{positions, velocities, accelerations, times}`

##### generate_joint_trajectory()

```python
generate_joint_trajectory(
    start_angles: Union[List[float], np.ndarray],
    goal_angles: Union[List[float], np.ndarray],
    duration: float = 1.0
) -> Dict[str, np.ndarray]
```

生成关节空间轨迹。

##### generate_cubic_trajectory()

```python
generate_cubic_trajectory(
    start: Union[List[float], np.ndarray],
    goal: Union[List[float], np.ndarray],
    start_vel: float = 0.0,
    goal_vel: float = 0.0,
    duration: float = 1.0
) -> Dict[str, np.ndarray]
```

生成三次多项式轨迹。

##### smooth_trajectory()

```python
smooth_trajectory(
    trajectory: Dict[str, np.ndarray],
    smoothing_factor: float = 0.1
) -> Dict[str, np.ndarray]
```

平滑轨迹。

---

## 工具函数

### 版本信息

```python
import embodiedai

print(embodiedai.__version__)  # 版本号
print(embodiedai.__author__)   # 作者
```

---

**需要更多帮助？** 查看 [示例代码](../examples/) 或提交 [Issue](https://github.com/ENDcodeworld/EmbodiedAI-Core/issues)。
