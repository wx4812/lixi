
---

### Week 10：Docker 概念与 OpenCV 实验
```markdown
# Week 10: Docker 概念与 OpenCV 实验

## 实验内容
本周完成了以下任务：
1. 深入学习 Docker 镜像、容器、分层存储等底层核心原理
2. 在 ROS2 Docker 容器中完整安装、配置 OpenCV 计算机视觉环境
3. 实现 ROS2 话题图像接收、OpenCV 图像处理与视觉算法验证

## 运行命令
```bash
# 容器内安装 OpenCV 视觉库
pip install opencv-python

# 运行 ROS2 + OpenCV 图像处理节点
ros2 run opencv_vision image_process_node
