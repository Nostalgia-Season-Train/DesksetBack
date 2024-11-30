from fastapi import APIRouter

from deskset.presenter.format import format_return
from deskset.feature.current import current

router_datetime = APIRouter(prefix='/v0/datetime', tags=['日期时间'])


@router_datetime.get('/date')
async def get_date():
    return format_return(current.date_format())

@router_datetime.get('/week')
async def get_week():
    return format_return(current.date_format())

@router_datetime.get('/time')
async def get_time():
    return format_return(current.time_format())

@router_datetime.get('/time12')
async def get_time12():
    return format_return(current.time_hour12_format())
