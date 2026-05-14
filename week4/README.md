### Week 4：命令行、机器人基础与 Python 仿真
```markdown
# Week 4: 命令行、机器人基础与 Python 仿真

## 实验内容
本周完成了以下任务：
1. Linux、ROS2 进阶常用命令行操作练习
2. 机器人运动控制与底层基础原理学习
3. 使用 Python 编写 ROS2 自定义节点，完成简易机器人运动仿真

## 运行命令
```bash
# 创建 Python 类型 ROS2 功能包
ros2 pkg create --build-type ament_python robot_py_demo

# 编译工作空间
colcon build

# 运行自定义 Python 仿真运动节点
ros2 run robot_py_demo move_control_node
