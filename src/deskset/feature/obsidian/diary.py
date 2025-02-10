from typing import Optional

from deskset.core.standard import DesksetError

from pathlib import Path
from deskset.core.root_path import RootPath
from deskset.core.text_file import TextFile


class Diary:
    def __init__(self, vault_path: str) -> None:
        if not Path(Path(vault_path) / '.obsidian').is_dir():
            raise DesksetError(message=f'{vault_path} 不是 Obsidian 仓库')

        # 读取 Obsidian 仓库配置
        from .vault_config.vault import ConfigVault
        from .vault_config.thino import ConfigVaultPlugin
        conf_vault  = ConfigVault(vault_path)
        conf_plugin = ConfigVaultPlugin(vault_path)

        # 设置要操作的 Obsidian 仓库
        from .obsidian import ObsidianManager
        self._obsidian = ObsidianManager(vault_path)

        # Root：日记目录；File：当前日记
        self._root = RootPath(str(Path(vault_path) / conf_vault.diary_folder))
        self._file = None

        # 解析器
        from ..note.diary    import DiaryParser
        from ..note.note     import NoteParser
        from ..note.activity import ActivityParser
        self._diary    = DiaryParser(conf_vault.diary_format + '.md')  # Obsidian 日期格式没有后缀
        self._note     = NoteParser()
        self._activity = ActivityParser(conf_plugin.activity_heading, conf_plugin.activity_format)

    # 列出一个月中的日记：date 格式 YYYYMM
    def list_a_month(self, date: str) -> list:
        return self._diary.get_diarys_in_a_month(self._root.get_files(), date)

    # === 读写日记前，先选择日记 ===

    # 选择日记：date 格式 YYYYMMDD
    def choose(self, date: str) -> None:
        path = self._root.calc_abspath(self._diary.get_diary_relpath(date))

        if Path(path).is_file():
            self._file = TextFile(path)
        else:
            self._file = None

    # 在 Obsidian 中打开日记
    def open_in_obsidian(self) -> None:
        if self._file is not None:
            self._obsidian.open_note_by_path(self._file.path())

    # 读取日记
    def read(self) -> dict:
        if self._file is not None:
            meta, content = self._note.metadata_and_content(self._file)
            return {
                'meta': meta,
                'content': content
            }
        else:
            return {
                'meta': '',
                'content': ''
            }

    # 读取日记中的动态
    def read_activitys(self) -> list:
        if self._file is not None:
            return self._activity.get_activitys(self._file)
        else:
            return []


# 适用于没有设置好 Obsidian 仓库的情况
class EmptyDiary():
    def __init__(self, vault_path: str) -> None:
        pass

    def list_a_month(self, date: str) -> list:
        return []

    def choose(self, date: str) -> None:
        pass

    def open_in_obsidian(self) -> None:
        pass

    def read(self) -> dict:
        return {
            'meta': '',
            'content': ''
        }

    def read_activitys(self) -> list:
        return []
