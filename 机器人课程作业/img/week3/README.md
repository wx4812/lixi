
---

### Week 3：GitHub SSH、VS Code 与 ROS2 交互
```markdown
# Week 3: GitHub SSH、VS Code 与 ROS2 交互

## 实验内容
本周完成了以下任务：
1. 配置 GitHub SSH 免密登录
2. VS Code 远程连接 WSL Ubuntu 开发环境
3. 实现 VS Code 端内 ROS2 工程创建、编译与交互调试

## 运行命令
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 测试 GitHub SSH 连通
ssh -T git@github.com

# VS Code 打开当前 WSL 工作目录
code .
