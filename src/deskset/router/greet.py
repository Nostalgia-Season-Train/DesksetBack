from fastapi import APIRouter

from deskset.presenter.format import format_return
from deskset.feature.greet import greet

router_greet = APIRouter(prefix='/v0/greet', tags=['问候'])


# 简单问候
@router_greet.get('/simple')
async def get_simple_greet():
    return format_return(greet.greet_simple())
