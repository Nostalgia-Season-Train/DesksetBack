from typing import Optional

from deskset.core.standard import DesksetError

from pathlib import Path
from deskset.core.root_path import RootPath


class Recent:
    def __init__(self, vault_path: str, encode: str = 'utf-8') -> None:
        if not Path(Path(vault_path) / '.obsidian').is_dir():
            raise DesksetError(message=f'{vault_path} 不是 Obsidian 仓库')
        self._vault = vault_path

        self._encode = encode

    def recent_open(self) -> list:
        workspace = Path(self._vault) / '.obsidian/workspace.json'
        if workspace.is_file():
            with open(workspace, 'r', encoding=self._encode) as file:
                import json
                data: dict = json.load(file)
                return data.get('lastOpenFiles', [])
        else:
            return []


if __name__ == '__main__':
    recent = Recent('')
    print(recent.recent_open())
