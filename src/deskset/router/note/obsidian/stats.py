from fastapi import APIRouter
from ..noteapi import noteapi

router_stats = APIRouter(prefix='/stats')

@router_stats.get('/note-number')
async def note_number():
    return (await noteapi.get(f'/stats/note-number')).json()

@router_stats.get('/heatmap')
async def heatmap():
    return (await noteapi.get(f'/stats/heatmap/7')).json()

@router_stats.get('/use-days')
async def use_days():
    return (await noteapi.get(f'/stats/use-days')).json()
