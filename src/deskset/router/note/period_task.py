from fastapi import APIRouter, Depends

from deskset.feature.apscheduler import apscheduler
from deskset.router.stand import DesksetRepJSON

from .noteapi import noteapi

router_period_task = APIRouter(
    prefix='/period-task', tags=['Period Task'],
    default_response_class=DesksetRepJSON
)

@router_period_task.get('/add-hello-task')
async def hello_task():
    async def hello():
        import asyncio
        asyncio.create_task(noteapi.get('/obsidian/hello'))
    apscheduler.add_job(hello, 'interval', seconds=5)
    return '添加 hello task 成功'
