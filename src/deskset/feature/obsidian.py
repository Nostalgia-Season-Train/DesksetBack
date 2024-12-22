import os
from time import sleep

WAIT_TIME = 0.25  # 执行一次命令后的等待时间，必须加上，否则命令来不及执行完就结束


class ObsidianManager:
    def __init__(self, path):
        self._vault_path = path  # 仓库路径

    def open_vault(self):
        os.startfile(f'obsidian://open?path={ self._vault_path }')
        sleep(WAIT_TIME)

    # name 是笔记名称
    def open_note_by_name(self, name):
        os.startfile(f'obsidian://open?path={ self._vault_path }/{ name }')
        sleep(WAIT_TIME)

    # path 是绝对路径
    def open_note_by_path(self, path):
        os.startfile(f'obsidian://open?path={ path }')
        sleep(WAIT_TIME)
