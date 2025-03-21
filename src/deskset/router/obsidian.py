# === Obsidian ===
from deskset.core.standard import DesksetError

from deskset.feature.obsidian.diary import Diary
from deskset.feature.obsidian.search import Search
from deskset.feature.obsidian.recent import Recent

from deskset.feature.obsidian.obsidian import ObsidianManager

from deskset.feature.conf_app import ConfApp, ConfAppObserver, conf_app

class Obsidian(ConfAppObserver):
    def __init__(self, conf_app: ConfApp) -> None:
        conf_app.attach(self)
        self.refresh(conf_app.obsidian_vault)

    def update(self, conf_app: ConfApp) -> None:
        # 仅当 仓库路径 实际变化，才会重新创建实例，避免数据意外刷新
        if self.vault != conf_app.obsidian_vault:
            self.refresh(conf_app.obsidian_vault)

    def refresh(self, vault_path: str) -> None:
        try:
            self.vault = vault_path

            self.diary = Diary(vault_path)
            self.search = Search(vault_path)
            self.recent = Recent(vault_path)

            self.manager = ObsidianManager(vault_path)

            self.is_init = True
        except DesksetError as error:
            self.is_init = False
            self.error = error

obsidian = Obsidian(conf_app)

def check_init() -> None:
    if obsidian.is_init is False:
        raise obsidian.error

# 注意：不要用 diary = obsidian.diary！
  # 因为这样 diary 指向 obsidian._diary 保存的实例，而不是 obsidian._diary 本身
  # 所以 diary 不会随 obsidian._diary 变化而变化
  # 哪怕设置更新成功，访问 diary 还是指向上个仓库中的日记


# === 路由 ===
from fastapi import APIRouter, Depends, Query
from deskset.presenter.format import format_return

from deskset.router.access import check_token


# 创建路由
router_obsidian = APIRouter(
    prefix='/v0/obsidian', tags=['Obsidian'],
    dependencies=[Depends(check_token), Depends(check_init)]
)

router_diary = APIRouter(prefix='/diary')
router_search = APIRouter(prefix='/search')
router_recent = APIRouter(prefix='/recent')

router_manager = APIRouter(prefix='/manager')


# 路由：日记

# 列出一个月中的日记
@router_diary.get('/list-a-month/{date}')
def list_a_month(date):
    return format_return(obsidian.diary.list_a_month(date))

# 打开 -> 选择日记
@router_diary.get('/open/{date}')
def open(date):
    return format_return(obsidian.diary.choose(date))

# 在 Obsidian 中打开日记
@router_diary.get('/open-in-obsidian')
def open_in_obsidian():
    return format_return(obsidian.diary.open_in_obsidian())

# 返回日记全部内容
@router_diary.get('/content')
def read():
    return format_return(obsidian.diary.read())

# 返回日记中的动态
@router_diary.get('/activity')
def read_activity():
    return format_return(obsidian.diary.read_activitys())


# 路由：搜索

# 在 Obsidian 中查找笔记
@router_search.get('/find-note')
def find_note(query: str = Query(None)):
    if query == '':  # 空字符串视作 None，即结束查询的标志。注：/find-note 传入 None，/find-note?query= 传入 ''
        query = None
    return format_return(obsidian.search.search(query))

# 在 Obsidian 中打开笔记
@router_search.get('/open-note/{relpath:path}')
def open_note(relpath: str):
    return format_return(obsidian.search.open_in_obsidian(relpath))


# 路由：最近笔记

# 最近打开
@router_recent.get('/recent-open')
def recent_open():
    return format_return(obsidian.recent.recent_open())


# 路由：管理

# 在 Obsidian 中打开笔记
@router_manager.get('/open-note/{relpath:path}')
def open_note(relpath: str):
    return format_return(obsidian.manager.open_note_by_relpath(relpath))


# 注册路由
router_obsidian.include_router(router_diary)
router_obsidian.include_router(router_search)
router_obsidian.include_router(router_recent)

router_obsidian.include_router(router_manager)
