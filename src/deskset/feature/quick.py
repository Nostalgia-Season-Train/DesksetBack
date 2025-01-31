import subprocess
import webbrowser
from pathlib import Path

def open_app_by_path(appPath: str):
    # 1、需要设置应用工作路径 cwd = 应用所在目录，否则某些应用无法运行
    # 2、如果应用随程序结束而关闭，这是 vsc 的原因，用命令行运行 .py 即可
    appCwd = Path(appPath).parent
    subprocess.Popen(appPath, cwd=appCwd)

def open_web_by_url(webUrl: str):
    webbrowser.open_new_tab(webUrl)
