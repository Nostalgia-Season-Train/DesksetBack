from fastapi import APIRouter, Depends

from deskset.router.access import check_token

router_note = APIRouter(
    prefix='/v0/note',
    dependencies=[Depends(check_token)]
)


# 注册子路由
from .obsidian import router_obsidian

router_note.include_router(router_obsidian)
