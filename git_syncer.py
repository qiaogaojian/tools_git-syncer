import os
import sys
import traceback
import yaml
import time
import argparse
import subprocess
import threading
from pycore.base import Core
from pycore.logger import Logger


# ********************************* 加载配置 *********************************
def load_config():
    """ 加载自动运行配置 """
    file_name = get_cur_file_name()
    config_path = f"{file_name}.yml"
    with open(get_full_relative_path(config_path), 'r', encoding='utf-8') as file:
        config = file.read()
        return yaml.safe_load(config)


def get_cur_file_name():
    """ 获取当前文件名字, 不带后缀 """
    cur_file_name = os.path.basename(os.path.realpath(sys.argv[0]))
    if '.' in cur_file_name:
        cur_file_name = cur_file_name.split('.')[0]
    return cur_file_name


def get_full_relative_path(relative_path):
    """ 生成基于当前脚本路径的相对路径. """
    cur_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    full_relative_path = f"{cur_file_path}/{relative_path}"
    return full_relative_path


# ********************************* 自动启动 *********************************
def run_init_command(arg_commands, config_commands):
    arg_commands.extend(config_commands)
    for command in arg_commands:
        Logger.instance().info(f"启动命令: \"{command}\"")
        threading.Thread(target=run_command, args=(command,)).start()


def run_command(command):
    """ 运行命令行 """
    try:
        os.chdir(get_full_relative_path('.'))
        # os.system(command)
        res = subprocess.call(command, creationflags=0x08000000, shell=True, stdout=subprocess.PIPE)  # 隐藏执行每一项指令
        output = res.stdout.decode('utf-8').strip()
        Logger.instance().info(output)
    except Exception as e:
        Logger.instance().info(f"run_command Exception:{e} trackback:{traceback.format_exc()}")


# ********************************* 自动同步 *********************************
def sync_repo(arg_paths, config_paths):
    arg_paths.extend(config_paths)
    for path in arg_paths:
        Logger.instance().info(f"同步仓库目录: \"{path}\"")
    Logger.instance().info(f"时间间隔:{interval}")

    sync_git_repo(arg_paths, interval)


def sync_git_repo(paths, interval):
    """ 同步 git 仓库."""
    if paths is None or len(paths) == 0:
        return

    while True:
        for path in paths:
            try:
                run_git_sync_cmd(path)
            except Exception as e:
                Logger.instance().info(f"sync_git_repo Exception:{e} trackback:{traceback.format_exc()}")
            time.sleep(3)

        time.sleep(interval)


def run_git_sync_cmd(path):
    """ 生成git指令并执行 """
    os.chdir(path)

    time_str = get_time()
    order_arr = ["git pull", "git status", "git add .", "git commit -m " + '"' + path + ' ' + time_str + '"', "git push"]  # 创建指令集合
    for order in order_arr:
        # os.system(order)
        res = subprocess.call(order, creationflags=0x08000000, stdout=subprocess.PIPE)  # 隐藏执行每一项指令
        output = res.stdout.decode('utf-8').strip()
        Logger.instance().info(output)


def get_time():
    """ 获取当前时间 """
    return time.ctime()


if __name__ == "__main__":
    core = Core()
    core.init(env="dev")

    Core.instance().logger.info('********************************* Git Syncer *********************************')

    config = load_config()

    command_config = config['command']
    path_config = config['path']
    interval = config['interval']
    if interval is None:
        interval = 1800

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    #  https://stackoverflow.com/questions/54022135/passing-an-array-into-python-argument-from-bash
    parser.add_argument('-c', nargs='+', help='需要自启动的命令行, 支持多个, 用空格隔开', default=[])
    parser.add_argument('-p', nargs='+', help='需要同步的git仓库路径, 支持多个, 用空格隔开', default=[])
    args = parser.parse_args()

    run_init_command(args.c, command_config)
    sync_repo(args.p, path_config)
