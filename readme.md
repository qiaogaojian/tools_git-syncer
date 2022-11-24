# Git Syncer

## 功能

- 自动同步git仓库
- 自动运行命令 (可用于 自启动 和 服务检测)

## 使用

- Windows

新建快捷方式, 放入 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` 目录

## 打包

```sh
pyinstaller -F -w .\git_syncer.py --noconsole
```
