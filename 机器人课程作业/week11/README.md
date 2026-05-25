# Week 11: Docker VNC、PyBullet 与 OpenCV 环境配置

## 一、实验目的

本周实验主要学习使用 ROS2 桌面 VNC Docker 容器搭建可视化机器人开发环境，并在容器中安装 PyBullet、OpenCV 和 NumPy 等常用机器人仿真与视觉处理库。通过本次实验，我希望掌握 Docker 镜像查看、容器运行、依赖安装、容器保存为新镜像等操作，理解如何将配置好的实验环境保存下来，方便后续重复使用。

## 二、实验内容

本周完成了以下任务：

1. 查看本地已有 Docker 镜像。
2. 启动 ROS2 Humble 桌面 VNC 容器。
3. 通过浏览器访问容器图形界面。
4. 在容器中安装 PyBullet 仿真库。
5. 在容器中安装 OpenCV 视觉处理库。
6. 安装兼容版本的 NumPy。
7. 查看运行中的容器 ID。
8. 使用 `docker commit` 将配置好的容器保存为新镜像。

## 三、实验环境

- 操作系统：Windows + WSL Ubuntu
- 容器工具：Docker
- ROS2 镜像：ghcr.io/tiryoh/ros2-desktop-vnc:humble
- 机器人系统：ROS2 Humble
- 仿真库：PyBullet
- 视觉库：OpenCV
- 数值计算库：NumPy
- 图形访问方式：浏览器 VNC

## 四、Docker VNC 容器说明

本次实验使用的镜像为：

```text
ghcr.io/tiryoh/ros2-desktop-vnc:humble
