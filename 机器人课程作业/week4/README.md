# Week 4: 命令行、机器人基础与 Python 仿真

## 一、实验目的

本周实验主要学习 Linux 与 ROS2 的进阶命令行操作，理解机器人运动控制的基础原理，并使用 Python 编写 ROS2 自定义节点完成简易机器人运动仿真。通过本次实验，我希望进一步熟悉 ROS2 工作空间、功能包、节点运行和话题通信的基本流程，为后续机器人控制实验打下基础。

## 二、实验内容

本周完成了以下任务：

1. 练习 Linux 常用命令，例如 `cd`、`ls`、`mkdir`、`touch`、`cp`、`mv`、`rm` 等。
2. 练习 ROS2 常用命令，例如 `ros2 pkg`、`ros2 run`、`ros2 node list`、`ros2 topic list` 等。
3. 学习机器人运动控制中的线速度和角速度概念。
4. 创建 Python 类型 ROS2 功能包 `robot_py_demo`。
5. 编写自定义 Python 节点 `move_control_node`。
6. 使用 `colcon build` 编译 ROS2 工作空间。
7. 运行自定义节点，模拟机器人前进和旋转运动。
8. 整理运行截图并提交到 GitHub 仓库。

## 三、实验环境

- 操作系统：Windows + WSL Ubuntu 22.04
- 机器人系统：ROS2 Humble
- 编程语言：Python
- 构建工具：colcon
- 编辑器：VS Code
- 终端：Ubuntu Terminal

## 四、Linux 常用命令练习

Linux 命令行是机器人开发中非常重要的基础工具。通过命令行可以创建文件夹、管理文件、运行程序和查看系统状态。

常用命令示例：

```bash
pwd
ls
cd ~/ros2_ws
mkdir test_folder
touch test.py
cp test.py test_copy.py
mv test_copy.py demo.py
rm demo.py
