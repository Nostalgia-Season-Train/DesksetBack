# ==== 数字桌搭在笔记仓库中存放的配置 ====
  # 方便与仓库集成，不用切换仓库时切换配置
from typing import Optional
from pathlib import Path

from deskset.core.log import logging
from deskset.core.standard import DesksetError
from deskset.core.config import write_conf_file_abspath, read_conf_file_abspath

from .._check import check_vault


# ==== NoteAPI 配置 ====
class ConfNoteAPI:
    _confitem_noteapi_host: str
    _confitem_noteapi_port: int

    def __init__(self, vault_path: str) -> None:
        check_vault(vault_path)
        self._decoder = 'json'
        self._confabspath = str(Path(vault_path) / '.deskset' / 'noteapi.json')
        self._confitem_noteapi_host = '127.0.0.1'
        self._confitem_noteapi_port = 6528
        self._confitem_server_host = '127.0.0.1'
        self._confitem_server_port = 6527
        try:
            read_conf_file_abspath(self, self._decoder)
        except DesksetError as err:
            logging.error(err.message)
        finally:
            write_conf_file_abspath(self, self._decoder)
