# Week 3: GitHub SSH、VS Code 与 ROS2 交互

## 一、实验目的

本周实验主要学习 GitHub SSH 免密登录配置、VS Code 远程连接 WSL Ubuntu 开发环境，以及在 VS Code 中完成 ROS2 工程的创建、编译和运行。通过本次实验，我希望掌握代码托管、远程开发和 ROS2 工程管理的基本流程，为后续机器人课程作业提交和 ROS2 项目开发打好基础。

## 二、实验内容

本周完成了以下任务：

1. 生成 SSH 密钥并配置到 GitHub。
2. 测试 GitHub SSH 连接是否成功。
3. 使用 VS Code Remote WSL 插件连接 Ubuntu 环境。
4. 在 VS Code 中打开 ROS2 工作空间。
5. 创建 ROS2 Python 功能包。
6. 使用 `colcon build` 编译 ROS2 工程。
7. 运行 ROS2 节点并观察终端输出。
8. 将实验内容整理后提交到 GitHub 仓库。

## 三、实验环境

- 操作系统：Windows
- Linux 环境：WSL Ubuntu 22.04
- 开发工具：VS Code
- 远程开发插件：Remote - WSL
- 代码托管平台：GitHub
- 机器人系统：ROS2 Humble
- 构建工具：colcon

## 四、GitHub SSH 配置说明

GitHub SSH 可以让本地电脑和 GitHub 仓库之间通过密钥进行身份验证。配置成功后，执行 `git clone`、`git pull`、`git push` 等命令时不需要每次输入账号密码。

SSH 密钥通常包含两个文件：

1. 私钥：保存在本地电脑，不能上传或泄露。
2. 公钥：可以添加到 GitHub，用于身份验证。

本实验使用 `ed25519` 算法生成 SSH 密钥。

## 五、运行命令

### 1. 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
