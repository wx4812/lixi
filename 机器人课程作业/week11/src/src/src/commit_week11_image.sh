#!/bin/bash

echo "请先通过 docker ps 查看容器 ID"
echo "用法: bash src/commit_week11_image.sh <container_id>"

if [ -z "$1" ]; then
    echo "错误: 请提供容器 ID"
    exit 1
fi

docker commit "$1" ros2-pybullet-opencv:week11

echo "镜像已保存为 ros2-pybullet-opencv:week11"
