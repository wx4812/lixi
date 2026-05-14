
---

### Week 8：Docker 安装与 ROS2 桌面容器
```markdown
# Week 8: Docker 安装与 ROS2 桌面容器

## 实验内容
本周完成了以下任务：
1. Ubuntu/WSL 环境下 Docker 完整安装与基础配置
2. ROS2 官方镜像拉取、独立容器创建与启动
3. 配置容器图形界面转发，实现容器内 ROS2 桌面级仿真与可视化

## 运行命令
```bash
# 启动本地 Docker 后台服务
sudo service docker start

# 拉取 ROS2 Humble 桌面版官方镜像
docker pull osrf/ros:humble-desktop

# 运行 ROS2 容器并开启网络权限
docker run -it --net=host osrf/ros:humble-desktop
