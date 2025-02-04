from deskset.core.standard import DesksetError

from deskset.feature.obsidian.diary import Diary, EmptyDiary
from deskset.feature.conf_app import ConfApp, ConfAppObserver, conf_app

class DiaryManager(ConfAppObserver):
    def __init__(self, conf_app: ConfApp) -> None:
        conf_app.attach(self)
        self.refresh(conf_app.obsidian_vault)

    def update(self, conf_app: ConfApp) -> None:
        if self.vault != conf_app.obsidian_vault:
            self.refresh(conf_app.obsidian_vault)

    def refresh(self, vault_path: str) -> None:
        try:
            self.vault = vault_path
            self.diary = Diary(vault_path)
        except DesksetError:  # 后面改成 DesksetExcept
            self.diary = EmptyDiary(vault_path)

diary_manager = DiaryManager(conf_app)


from fastapi import APIRouter
from deskset.core.locale import _t
from deskset.presenter.format import format_return

router_diary = APIRouter(prefix='/v0/diary', tags=[_t('diary')])

# 列出一个月中的日记
@router_diary.get('/list-a-month/{date}')
def list_a_month(date):
    return format_return(diary_manager.diary.list_a_month(date))

# 打开 -> 选择日记
@router_diary.get('/open/{date}')
def open(date):
    return format_return(diary_manager.diary.choose(date))

# 在 Obsidian 中打开日记
@router_diary.get('/open-in-obsidian')
def open_in_obsidian():
    return format_return(diary_manager.diary.open_in_obsidian())

# 返回日记全部内容
@router_diary.get('/content')
def read():
    return format_return(diary_manager.diary.read())

# 返回日记中的动态
@router_diary.get('/activity')
def read_activity():
    return format_return(diary_manager.diary.read_activitys())
