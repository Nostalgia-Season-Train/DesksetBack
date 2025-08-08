from fastapi import APIRouter, Depends
from deskset.router.unify import DesksetReqNumberInt
from ._manager import api as noteapi

router_stats = APIRouter(prefix='/stats')

@router_stats.get('/note-number')
async def note_number():
    return await noteapi.get_note_number()
