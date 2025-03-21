from fastapi import APIRouter

from deskset.router.stand_response import DesksetJSONResponse

router_obsidian = APIRouter(
    prefix='/v0/obsidian', tags=['Obsidian']
)


# ==== 日记 ====
router_diary = APIRouter(prefix='/diary', default_response_class=DesksetJSONResponse)

@router_diary.get('/today')
def today():
    return 'today'


# ==== 注册 Obsidian 的子路由 ====
router_obsidian.include_router(router_diary)
