# === Obsidian ===
from deskset.core.standard import DesksetError

from deskset.feature.obsidian.diary import Diary, EmptyDiary
from deskset.feature.obsidian.search import Search, EmptySearch
from deskset.feature.conf_app import ConfApp, ConfAppObserver, conf_app

class Obsidian(ConfAppObserver):
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
            self.search = Search(vault_path)
        except DesksetError:  # - [ ] 改成 Depend 依赖项
            self.diary = EmptyDiary(vault_path)
            self.search = EmptySearch(vault_path)

obsidian = Obsidian(conf_app)

diary = obsidian.diary
search = obsidian.search


# === 路由 ===
from fastapi import APIRouter, Depends, Query
from deskset.presenter.format import format_return

from deskset.router.access import check_token


# 创建路由
router_obsidian = APIRouter(prefix='/v0/obsidian', tags=['Obsidian'], dependencies=[Depends(check_token)])
router_diary = APIRouter(prefix='/diary')
router_search = APIRouter(prefix='/search')


# 路由：日记

# 列出一个月中的日记
@router_diary.get('/list-a-month/{date}')
def list_a_month(date):
    return format_return(diary.list_a_month(date))

# 打开 -> 选择日记
@router_diary.get('/open/{date}')
def open(date):
    return format_return(diary.choose(date))

# 在 Obsidian 中打开日记
@router_diary.get('/open-in-obsidian')
def open_in_obsidian():
    return format_return(diary.open_in_obsidian())

# 返回日记全部内容
@router_diary.get('/content')
def read():
    return format_return(diary.read())

# 返回日记中的动态
@router_diary.get('/activity')
def read_activity():
    return format_return(diary.read_activitys())


# 路由：搜索

# 在 Obsidian 中查找笔记
@router_search.get('/find-note')
def find_note(query: str = Query()):
    return format_return(search.search(query))

# 在 Obsidian 中打开笔记
@router_search.get('/open-note/{relpath:path}')
def open_note(relpath: str):
    return format_return(search.open_in_obsidian(relpath))


# 注册路由
router_obsidian.include_router(router_diary)
router_obsidian.include_router(router_search)
