# Git Syncer

## 功能

- 自动同步git仓库
- 自动运行命令 (可用于 自启动 和 服务检测)

## 使用

- Windows

新建快捷方式, 放入 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` 目录


## 配置

打开同目录 git_syncer.yml 配置文件

```yaml
# 自启动命令
command:
  - 'pouchdb-server --port 3996 --dir D:\Git\Config\config_highlighter\db --config D:\Git\Config\config_highlighter\config.json --sqlite'

# 需要定时同步的git仓库地址
path:  
  - 'D:\Git\Config\config_highlighter'
  - 'D:\Git\Config\config_rime'
  - 'D:\Git\Config\config_vim'
  - 'C:\Users\Administrator\.vscode'
  - 'C:\Users\Administrator\AppData\Roaming\Code\User'

# 定时同步的时间间隔
interval: 18

```

## 打包

```sh
pyinstaller -F -w .\git_syncer.py --noconsole
```
