from fastapi import APIRouter, Depends

from deskset.core.config import config
from deskset.router.stand_response import DesksetJSONResponse

from .noteapi import noteapi
from .validate import DesksetReqDateDay

router_obsidian = APIRouter(
    prefix='/v0/obsidian', tags=['Obsidian']
)


# ==== 日记 ====
router_diary = APIRouter(prefix='/diary', default_response_class=DesksetJSONResponse)

@router_diary.get('/today')
async def today():
    diary = (await noteapi.get(f'/diary/read-today')).json()
    return diary

@router_diary.get('/today-tasks')
async def today_tasks():
    diary = (await noteapi.get(f'/diary/read-today')).json()
    diary_tasks = (await noteapi.post(f'/tasks/get-all-tasks', data={'notepath': diary['notepath']})).json()
    return diary_tasks

@router_diary.get('/read/{day}')
async def read(date: DesksetReqDateDay = Depends()):
    diary = (await noteapi.get(f'/diary/read/{date.day}')).json()
    return diary

@router_diary.get('/read-tasks/{day}')
async def read_tasks(date: DesksetReqDateDay = Depends()):
    diary = (await noteapi.get(f'/diary/read/{date.day}')).json()
    diary_tasks = (await noteapi.post(f'/tasks/get-all-tasks', data={'notepath': diary['notepath']})).json()
    return diary_tasks


# ==== 注册 Obsidian 的子路由 ====
router_obsidian.include_router(router_diary)
