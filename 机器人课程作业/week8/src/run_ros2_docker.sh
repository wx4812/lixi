#!/bin/bash

echo "启动 Docker 服务..."
sudo service docker start

echo "查看 Docker 版本..."
docker --version

echo "拉取 ROS2 Humble 桌面版镜像..."
docker pull osrf/ros:humble-desktop

echo "查看本地 Docker 镜像..."
docker images

echo "启动 ROS2 Humble Docker 容器..."
docker run -it --net=host osrf/ros:humble-desktop
