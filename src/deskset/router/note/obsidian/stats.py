from fastapi import APIRouter, Depends
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
