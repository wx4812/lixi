# Week 14：手机遥控 + 局域网通信 + turtlesim 迷宫探索

> AI 机器人课程 第14周 | 方向 B：turtlesim 二维乌龟迷宫 | 单人项目

## 控制链路

```
手机浏览器  →  Tailscale 局域网  →  WebSocket  →  turtlesim_web_bridge.py  →  ROS2 turtlesim
```

---

## 文件结构

```
week14/
├── src/
│   └── turtle_maze/              # ROS2 ament_python 包
│       ├── turtle_maze/
│       │   ├── __init__.py
│       │   ├── turtlesim_web_bridge.py   # 常驻主程序
│       │   ├── explorer.py               # 自动探索算法
│       │   └── index.html                # 手机遥控网页
│       ├── launch/
│       │   └── turtle_maze.launch.py     # 一键启动 launch 文件
│       ├── resource/
│       │   └── turtle_maze
│       ├── package.xml
│       ├── setup.py
│       └── setup.cfg
├── turtlesim_web_bridge.py       # 脚本模式（直接 python3 运行，无需编译）
├── explorer.py
├── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

> **两种运行方式均可：**
> - **脚本模式**：直接 `python3 turtlesim_web_bridge.py`（推荐，无需 colcon build）
> - **ROS2 包模式**：`colcon build` 后用 `ros2 launch turtle_maze turtle_maze.launch.py`

---

## 环境要求

- Ubuntu 22.04 / WSL2
- ROS2 Humble
- Python 3.10+
- Tailscale

---

## 方式一：脚本模式（推荐）

### 1. 安装 Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo service tailscaled start
sudo tailscale up
tailscale ip -4        # 记下此地址，如 100.x.y.z
```

### 2. 启动 turtlesim

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

### 3. 启动桥接程序（新终端）

```bash
source /opt/ros/humble/setup.bash
cd week14
pip install -r requirements.txt
python3 turtlesim_web_bridge.py
```

### 4. 手机打开遥控器

```
http://<Tailscale_IP>:8080
```

---

## 方式二：ROS2 包模式

```bash
# 在 ROS2 工作空间 src/ 下克隆或复制本仓库，然后：
cd ~/ros2_ws
colcon build --packages-select turtle_maze
source install/setup.bash
pip install aiohttp

# 一键启动（turtlesim + bridge）
ros2 launch turtle_maze turtle_maze.launch.py
```

---

## 功能说明

| 功能 | 说明 |
|------|------|
| ▲▼◀▶ 方向键 | 长按持续移动，松开立即停止 |
| 🤖 AUTO 按钮 | 切换自动探索模式（右手法则算法） |
| ↺ RESET | 乌龟回到起点，重置状态 |
| 实时迷宫地图 | 障碍墙、轨迹、起点/终点、乌龟朝向 |
| 碰撞检测 | 撞墙自动阻挡，乌龟变橙色提示 |
| 终点检测 | 到达终点弹出完成横幅 |

---

## 迷宫参数

| 项目 | 值 |
|------|----|
| 类型 | 4×4 完美迷宫（递归回溯生成，BFS验证有解） |
| 坐标系 | turtlesim 标准（0 ~ 11） |
| 起点 START | `(1.2, 1.2)` |
| 终点 GOAL | `(9.8, 9.8)` |
| 终点半径 | 0.6 |

---

## 自动探索算法（explorer.py）

**右手法则巡墙器（Right-Hand Wall Follower）**

```
状态机：check_right → turn_right → forward_right_probe
                ↓ 右侧被阻
         undo_right_turn → forward → check_right
                ↓ 前方被阻
              turn_left → forward
```

对完美迷宫（任意两点唯一通路），右手法则保证一定能走到终点。

---

## 工程原则

> 接收网络 + 控制机器人写在**同一个常驻程序**里（`turtlesim_web_bridge.py`），手机网页只负责发送命令，不额外启动第二个控制程序。

---

## 评分对应

| 评分维度 | 占比 | 实现 |
|----------|------|------|
| 链路打通 | 30% | ✅ 手机→Tailscale→WebSocket→ROS2 |
| 迷宫探索 | 25% | ✅ 4×4完美迷宫，碰撞+终点判定 |
| 进阶功能 | 25% | ✅ 右手法则自动探索（单人必做） |
| 工程规范 | 10% | ✅ 单一常驻程序，ROS2包结构规范 |
| 报告与展示 | 10% | 📝 见报告书 |
