from fastapi import APIRouter

from deskset.feature.diary import diary

router_diary = APIRouter(prefix='/diary', tags=['日记'])


@router_diary.get('/today')
async def get_today_diary():
    return diary.get_today_diary()

@router_diary.post('/create')
async def create_today_diary():
    return diary.create_today_diary()
