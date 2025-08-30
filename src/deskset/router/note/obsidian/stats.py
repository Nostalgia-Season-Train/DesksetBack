from fastapi import APIRouter, Depends
from pydantic import BaseModel, RootModel
from deskset.router.unify import DesksetReqNumberInt
from ._manager import api as noteapi

router_stats = APIRouter(prefix='/stats')

@router_stats.get('/note-number')
async def note_number():
    return await noteapi.get_note_number()

@router_stats.get('/attachment-number')
async def attachment_number():
    return await noteapi.get_attachment_number()

@router_stats.get('/useday-number')
async def useday_number():
    return await noteapi.get_useday_number()

@router_stats.get('/heatmap/{num}')
async def heatmap(req: DesksetReqNumberInt = Depends()):
    weeknum = req.num  # 统计范围：前 weeknum 周 + 本周
    return await noteapi.get_heatmap(weeknum)

# - [ ] 临时，后面转移到新路由
class Filter(BaseModel):
    type: str = 'contains'  # 比较类型：is、startsWith、endsWith、contains、isEmpty
    isInvert: bool = False  # 是否取反比较结果
    frontmatterKey: str     # 要比较的属性
    compareValue: str       # 要比较的值

# 注：OpenAPI 会误将 FilterList 识别为 str，实际工作正常
class FilterList(RootModel[list['Filter | FilterList']]):
    pass

# 注 1：filters 若为空数组返回 所有笔记
# 注 2：frontmatterKey 若为空字符串，该次 filter 返回 false
# 注 3：type 若不为上述五种类型，该次 filter 返回 false
@router_stats.post('/filter-frontmatter')
async def filter_frontmatter(filters: FilterList):
    return await noteapi.filter_frontmatter(filters.model_dump())  # type: ignore

@router_stats.post('/filter-frontmatter-number')
async def filter_frontmatter_number(filters: FilterList):
    return await noteapi.filter_frontmatter_number(filters.model_dump())  # type: ignore
