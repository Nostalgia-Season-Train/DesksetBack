from fastapi import APIRouter, Query

from ._manager import manager
from ._noteapi import noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/current-note')
async def get_current_note():
    return (await noteapi.get('/obsidian/current-note')).text

@router_common.get('/recent-notes')
async def get_recent_notes():
    workspace = (await noteapi.get('/obsidian/workspace')).json()
    recent_files = workspace.get('lastOpenFiles', []) if isinstance(workspace, dict) else []
    return [file for file in recent_files if isinstance(file, str) and file.endswith('.md')]

# 在 Obsidian 中打开笔记，笔记路径 notepath 以仓库为根目录
@router_common.get('/open')
def open(notepath: str = Query(None)):
    if (notepath == None):
        return
    from webbrowser import open
    open(f'obsidian://open?path={ manager.vault }/{ notepath }')
