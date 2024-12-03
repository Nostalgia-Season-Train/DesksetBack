import arrow
from fastapi import APIRouter
from pydantic import BaseModel

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.presenter.format import format_return
from deskset.feature.diary import Diary

diary = Diary(config.dir, config.format)
router_diary = APIRouter(prefix='/v0/diary', tags=[_t('diary')])

class Input(BaseModel):
    content: str


@router_diary.get('/read')
async def read_diary(date=arrow.now().format('YYYYMMDD')):
    return format_return(diary.read_diary(date))

@router_diary.post('/create')
async def create_diary(date=arrow.now().format('YYYYMMDD')):
    return format_return(diary.create_diary(date))

@router_diary.put('/write')
async def write_diary(input: Input, date=arrow.now().format('YYYYMMDD')):
    return format_return(diary.write_diary(date, input.content))

@router_diary.delete('/delete')
async def delete_diary(date=arrow.now().format('YYYYMMDD')):
    return format_return(diary.delete_diary(date))
