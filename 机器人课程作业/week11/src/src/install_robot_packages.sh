#!/bin/bash

echo "安装 PyBullet 仿真库..."
pip3 install pybullet --break-system-packages

echo "安装 OpenCV 视觉库..."
pip3 install opencv-python opencv-contrib-python --break-system-packages

echo "安装 NumPy 兼容版本..."
pip3 install "numpy<2" --break-system-packages

echo "依赖安装完成"
