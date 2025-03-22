from fastapi import APIRouter
from httpx import AsyncClient

from deskset.core.config import config
from deskset.router.stand_response import DesksetJSONResponse

router_obsidian = APIRouter(
    prefix='/v0/obsidian', tags=['Obsidian']
)


# ==== 日记 ====
router_diary = APIRouter(prefix='/diary', default_response_class=DesksetJSONResponse)

@router_diary.get('/today')
async def today():
    async with AsyncClient() as client:
        return (await client.get(f'http://{config.noteapi_host}:{config.noteapi_port}/diary/read-today')).text


# ==== 注册 Obsidian 的子路由 ====
router_obsidian.include_router(router_diary)
