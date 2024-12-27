# 日记
from pathlib import Path

from deskset.core.config import config

from deskset.feature.obsidian.obsidian import ObsidianManager
from deskset.feature.obsidian.config.vault import ConfigVault
from deskset.feature.obsidian.config.vault_plugin import ConfigVaultPlugin

from deskset.core.root_path import RootPath
from deskset.feature.diary  import DiaryParser

from deskset.core.text_file   import TextFile
from deskset.feature.note     import NoteParser
from deskset.feature.prose    import ProseParser
from deskset.feature.activity import ActivityParser
from deskset.feature.todo     import TodoParser

class Diary:
    def __init__(self):
        self._obsidian = ObsidianManager(config.obsidian_vault)
        vault_path = config.obsidian_vault
        conf_vault  = ConfigVault(vault_path)
        conf_plugin = ConfigVaultPlugin(vault_path)

        self._root  = RootPath(Path(vault_path) / conf_vault.diary_folder)
        self._diary = DiaryParser(conf_vault.diary_format + '.md')  # obsidian 日期格式没有后缀

        self._file     = TextFile()
        self._note     = NoteParser()
        self._prose    = ProseParser('# 随笔')
        self._activity = ActivityParser(conf_plugin.activity_heading, conf_plugin.activity_format)  # 动态配置，遵循 Thino
        self._todo     = TodoParser('# 打卡')

    # 日记列表
    def list(self):
        return self._diary.get_diarys(self._root.get_files())

    # 打开日记
    def open(self, date):
        """date 格式：YYYYMMDD"""
        if self._file.is_open():
            self._file.close()
        self._file.open(self._root.get_abspath(self._diary.get_diary_relpath(date)))

    # 关闭日记
    def close(self):
        self._file.close()

    # 用 obsidian 打开日记
    def open_in_obsidian(self):
        self._obsidian.open_note_by_path(self._file.path())

    # 日记
    def read(self):
        meta, content = self._note.metadata_and_content(self._file)
        return {
            'meta': meta,
            'content': content
        }

    # 随笔
    def read_prose(self):
        return self._prose.get_prose(self._file)

    # 动态
    def read_activitys(self):
        return self._activity.get_activitys(self._file)

    # 打卡
    def read_todos(self):
        return self._todo.get_todos(self._file)

diary = Diary()


# 路由
from fastapi import APIRouter

from deskset.core.locale import _t
from deskset.presenter.format import format_return

router_diary = APIRouter(prefix='/v0/diary', tags=[_t('diary')])

# 日记列表
@router_diary.get('/list')
def list():
    return format_return(diary.list())

# 打开日记
@router_diary.get('/open/{date}')
def open(date):
    return format_return(diary.open(date))

# 关闭日记
@router_diary.get('/close')
def close():
    return format_return(diary.close())

# 用 Obsidian 打开日记
@router_diary.get('/open-in-obsidian')
def open_in_obsidian():
    return format_return(diary.open_in_obsidian())

# 日记
@router_diary.get('/content')
def read():
    return format_return(diary.read())

# 随笔
@router_diary.get('/prose')
def read_prose():
    return format_return(diary.read_prose())

# 动态
@router_diary.get('/activity')
def read_activity():
    return format_return(diary.read_activitys())

# 打卡
@router_diary.get('/todo')
def read_todo():
    return format_return(diary.read_todos())
