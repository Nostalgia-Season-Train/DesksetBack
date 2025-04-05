from fastapi import APIRouter
from deskset.router.unify import DesksetRepJSON

router_obsidian = APIRouter(
    prefix='/obsidian', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)

# 日记
from .diary import router_diary
router_obsidian.include_router(router_diary)

# 数据统计
from .stats import router_stats
router_obsidian.include_router(router_stats)

# 搜索
from .search import router_search
router_obsidian.include_router(router_search)
