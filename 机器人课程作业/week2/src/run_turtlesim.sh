#!/bin/bash

source /opt/ros/humble/setup.bash

echo "启动 turtlesim 键盘控制节点"
ros2 run turtlesim turtle_teleop_key
