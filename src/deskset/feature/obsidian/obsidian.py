import os
from time import sleep

from deskset.core.standard import DesksetError

from pathlib import Path

WAIT_TIME = 0.15  # 执行一次命令后的等待时间，必须加上，否则命令来不及执行完就结束


class ObsidianManager:
    def __init__(self, vault_path: str) -> None:
        if not Path(Path(vault_path) / '.obsidian').is_dir():
            raise DesksetError(message=f'{vault_path} 不是 Obsidian 仓库')
        self._vault = vault_path

    def open_vault(self) -> None:
        os.startfile(f'obsidian://open?path={ self._vault }')
        sleep(WAIT_TIME)

    # name 是笔记名称
    def open_note_by_name(self, name: str) -> None:
        os.startfile(f'obsidian://open?path={ self._vault }/{ name }')
        sleep(WAIT_TIME)

    # path 是绝对路径
    def open_note_by_path(self, path: str) -> None:
        os.startfile(f'obsidian://open?path={ path }')
        sleep(WAIT_TIME)

    # relpath 以仓库为根路径
    def open_note_by_relpath(self, relpath: str) -> None:
        if not (Path(self._vault) / relpath).is_file():
            raise DesksetError(message=f'{relpath} 笔记不存在')
        os.startfile(f'obsidian://open?path={ self._vault }/{ relpath }')
        sleep(WAIT_TIME)


if __name__ == '__main__':
    manager = ObsidianManager('')
