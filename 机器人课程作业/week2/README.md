# Week 2：WSL、Ubuntu 与 ROS2 环境配置

## 一、实验目的

本周实验主要完成 WSL、Ubuntu 22.04 和 ROS2 Humble 的安装与环境配置，并通过运行 turtlesim 小乌龟仿真程序验证 ROS2 是否安装成功。通过本次实验，我希望掌握 Linux 终端的基本使用方法，理解 ROS2 的节点运行方式，并熟悉后续机器人课程所需要的基础开发环境。

## 二、实验内容

本周完成了以下任务：

1. 在 Windows 系统中安装并启用 WSL。
2. 安装 Ubuntu 22.04 子系统。
3. 配置 ROS2 Humble 软件源和运行环境。
4. 安装 ROS2 常用工具包。
5. 运行 turtlesim 小乌龟仿真节点。
6. 使用键盘控制节点控制小乌龟移动。
7. 通过实验截图记录环境配置和运行结果。

## 三、实验环境

- 操作系统：Windows
- Linux 子系统：Ubuntu 22.04
- 机器人系统：ROS2 Humble
- 终端工具：Windows Terminal / Ubuntu Terminal
- 测试程序：turtlesim

## 四、WSL 与 Ubuntu 简介

WSL 是 Windows Subsystem for Linux 的缩写，可以让用户在 Windows 系统中直接运行 Linux 环境。相比虚拟机，WSL 启动更快，占用资源更少，适合进行 Linux 命令学习、机器人开发和 ROS2 环境配置。

Ubuntu 是常用的 Linux 发行版之一，ROS2 Humble 官方推荐使用 Ubuntu 22.04，因此本次实验选择 Ubuntu 22.04 作为基础环境。

## 五、ROS2 简介

ROS2 是 Robot Operating System 2 的缩写，是机器人开发中常用的软件框架。它提供了节点、话题、服务、参数等通信机制，可以帮助开发者快速构建机器人系统。

在 ROS2 中，节点是执行具体功能的程序。例如 turtlesim_node 负责显示小乌龟仿真界面，turtle_teleop_key 节点负责接收键盘输入并发布控制指令。两个节点通过话题进行通信，从而实现键盘控制小乌龟移动。

## 六、运行命令

启动小乌龟仿真节点：

```bash
ros2 run turtlesim turtlesim_node
