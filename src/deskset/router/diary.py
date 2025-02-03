from deskset.feature.obsidian.diary import Diary
from deskset.feature.obsidian.config import config_app_obsidian

diary = Diary(config_app_obsidian.obsidian_vault)


from fastapi import APIRouter
from deskset.core.locale import _t
from deskset.presenter.format import format_return

router_diary = APIRouter(prefix='/v0/diary', tags=[_t('diary')])

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
