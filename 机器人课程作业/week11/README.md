# 1. 查看本地已有的Docker镜像
docker images

# 2. 启动ROS2桌面VNC容器
docker run -p 6080:80 --security-opt seccomp=unconfined --shm-size=512m \
-v "$(pwd):/home/ws" \
ghcr.io/tiryoh/ros2-desktop-vnc:humble

# 3. 在容器VNC终端内安装依赖
# 安装pybullet仿真库
pip3 install pybullet --break-system-packages

# 安装opencv视觉相关库
pip3 install opencv-python opencv-contrib-python --break-system-packages

# 安装numpy数值运算库
pip3 install "numpy<2" --break-system-packages

# 4. 新开宿主机终端，查看运行中的容器ID
docker ps

# 5. 将配置好的容器保存为新镜像
docker commit <你的容器ID> ros2-pybullet-opencv:week11
