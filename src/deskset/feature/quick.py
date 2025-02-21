import subprocess
import webbrowser
from pathlib import Path

import platform

SYSTEM = platform.system()


def open_app_by_path(appPath: str):
    # 1、需要设置应用工作路径 cwd = 应用所在目录，否则某些应用无法运行
    # 2、如果应用随程序结束而关闭，这是 vsc 的原因，用命令行运行 .py 即可
    appCwd = Path(appPath).parent
    subprocess.Popen(appPath, cwd=appCwd)

def open_web_by_url(webUrl: str):
    webbrowser.open_new_tab(webUrl)

# 打开回收站
def open_recycle():
    if SYSTEM == 'Windows':
        subprocess.Popen('explorer shell:RecycleBinFolder', shell=True)
        # subprocess.Popen('start shell:RecycleBinFolder', shell=True)  # 会使已经打开的回收站消失
        # os.system('start shell:RecycleBinFolder')  # 打包后运行会弹出 CMD 窗口
