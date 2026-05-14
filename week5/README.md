### Week 5：Linux 目录操作与机器人运动学
```markdown
# Week 5: Linux 目录操作与机器人运动学

## 实验内容
本周完成了以下任务：
1. Linux 目录层级、文件权限、批量管理进阶操作
2. 机器人正运动学、逆运动学基础理论学习
3. 在 ROS2 中完成运动学模型计算与数据验证

## 运行命令
```bash
# Linux 目录与权限常用操作
ls -la
mkdir kinematics_ws
chmod +x calc_script.py

# 运行运动学计算验证节点
ros2 run kinematics_demo kinematic_solver

