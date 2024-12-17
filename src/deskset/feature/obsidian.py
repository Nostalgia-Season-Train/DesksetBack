import os
from time import sleep

WAIT_TIME = 0.25  # 执行一次命令后的等待时间，必须加上，否则命令来不及执行完就结束


class ObsidianManager:
    def __init__(self, path):
        self._vault_path = path  # 仓库路径

    def open_vault(self):
        os.startfile(f'obsidian://open?path={ self._vault_path }')
        sleep(WAIT_TIME)

    # 打开笔记，note 既可以是 name 也可以是 path/to/name（去掉后缀）
    def open_note(self, note):
        os.startfile(f'obsidian://open?path={ self._vault_path }/{ note }')
        sleep(WAIT_TIME)
