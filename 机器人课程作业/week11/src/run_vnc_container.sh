#!/bin/bash

echo "启动 ROS2 Humble VNC 桌面容器..."

docker run -p 6080:80 \
  --security-opt seccomp=unconfined \
  --shm-size=512m \
  -v "$(pwd):/home/ws" \
  ghcr.io/tiryoh/ros2-desktop-vnc:humble
