from fastapi import APIRouter
from ..noteapi import noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/current-note')
async def get_current_note():
    return (await noteapi.get('/obsidian/current-note')).text

@router_common.get('/recent-notes')
async def get_recent_notes():
    workspace = (await noteapi.get('/obsidian/workspace')).json()
    recent_files = workspace.get('lastOpenFiles', []) if isinstance(workspace, dict) else []
    return [file for file in recent_files if isinstance(file, str) and file.endswith('.md')]
