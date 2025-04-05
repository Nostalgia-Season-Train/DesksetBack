from fastapi import APIRouter

from ._manager import manager

router_profile = APIRouter(prefix='/profile')

@router_profile.get('/data')
def get_data():
    return {
        'name': manager.conf_profile._confitem_name,
        'bio': manager.conf_profile._confitem_bio
    }
