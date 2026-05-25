# Week 8: Docker 安装与 ROS2 桌面容器

## 一、实验目的

本周实验主要学习在 Ubuntu/WSL 环境下安装和配置 Docker，并使用 ROS2 Humble 官方桌面版镜像创建容器环境。通过本次实验，我希望理解 Docker 镜像、容器和宿主机之间的关系，掌握使用 Docker 快速搭建 ROS2 实验环境的方法，并尝试配置图形界面转发，实现容器内 ROS2 桌面级仿真与可视化。

## 二、实验内容

本周完成了以下任务：

1. 在 Ubuntu/WSL 环境中安装 Docker。
2. 启动 Docker 后台服务并测试 Docker 是否可用。
3. 拉取 ROS2 Humble 桌面版官方镜像。
4. 使用 Docker 创建并进入 ROS2 容器。
5. 理解 Docker 镜像和容器的区别。
6. 配置容器网络参数，方便 ROS2 节点通信。
7. 尝试运行 ROS2 桌面工具和图形化程序。
8. 记录实验过程、运行截图和遇到的问题。

## 三、实验环境

- 操作系统：Windows + WSL Ubuntu 22.04
- 容器工具：Docker
- ROS2 镜像：osrf/ros:humble-desktop
- 机器人系统：ROS2 Humble
- 终端工具：Ubuntu Terminal
- 可视化工具：RViz2 / turtlesim

## 四、Docker 基础概念

Docker 是一种容器化工具，可以将程序运行所需的系统环境、依赖库和应用程序打包到镜像中。使用 Docker 后，即使换到另一台电脑，也可以通过相同镜像快速创建一致的运行环境。

### 1. 镜像

镜像可以理解为一个只读模板，里面包含操作系统、软件依赖和程序环境。例如 `osrf/ros:humble-desktop` 就是一个已经安装好 ROS2 Humble 桌面环境的镜像。

### 2. 容器

容器是镜像运行后的实例。一个镜像可以创建多个容器，每个容器之间相互隔离。

### 3. Dockerfile

Dockerfile 是构建自定义镜像的脚本文件，可以写入安装依赖、复制文件和启动程序等命令。

## 五、ROS2 Docker 镜像说明

本次实验使用的镜像是：

```text
osrf/ros:humble-desktop
