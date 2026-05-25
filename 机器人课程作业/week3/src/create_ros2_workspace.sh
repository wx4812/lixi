#!/bin/bash

source /opt/ros/humble/setup.bash

echo "创建 ROS2 工作空间..."
mkdir -p ~/ros2_ws/src

echo "进入 src 目录..."
cd ~/ros2_ws/src || exit

echo "创建 ROS2 Python 功能包 week3_demo..."
ros2 pkg create --build-type ament_python week3_demo

echo "返回工作空间并编译..."
cd ~/ros2_ws || exit
colcon build

echo "加载工作空间环境..."
source install/setup.bash

echo "ROS2 工作空间创建与编译完成"
