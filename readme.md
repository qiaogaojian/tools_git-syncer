# Git Syncer

## 功能

- 开机启动
- 定期同步git仓库

## 使用

- Windows

打开 release 文件夹, 给 git_syncer.exe 创建快捷方式, 放入 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` 目录

## 配置

打开同目录 git_syncer.yml 配置文件

```yaml
# 自启动命令
command:
  - 'D:\Program\syncthing-windows-amd64-v1.23.5\syncthing.exe --no-console --no-browser'

# 需要定时同步的git仓库地址
path:  
  - '%HOMEPATH%\.vscode'
  - '%HOMEPATH%\AppData\Roaming\Code\User'
  - 'D:\Git\Config\config_vim'
  - 'D:\Git\Config\config_ahk'
  - 'D:\Git\Config\config_highlighter'

# 定时同步的时间间隔 以秒为单位
interval: 18

```

## 打包

```sh
# 安装打包工具
pip install pyinstaller config --global http.sslVerify false

# 打包 打包后的可执行文件在 dist目录
pyinstaller -F -w .\git_syncer.py --noconsole
```
