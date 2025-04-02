from fastapi import APIRouter, Depends

import deskset.feature.quick as quick

from deskset.router.unify import check_token
from deskset.router.unify import DesksetReqPath, DesksetReqFolder, DesksetReqURL
from deskset.router.unify import DesksetRepJSON

router_quick = APIRouter(
    prefix='/v0/quick', tags=['快速启动'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)

@router_quick.get('/open-default/{path:path}')
def open_default(req: DesksetReqPath = Depends()):
    return quick.open_default(req.path)

@router_quick.post('/open-app-through-path')
def open_app_through_path(req: DesksetReqPath):
    quick.open_app_by_path(req.path)
    return '成功打开应用：{}'.format(req.path)

@router_quick.post('/open-web-through-url')
def open_web_through_url(req: DesksetReqURL):
    quick.open_web_by_url(req.url)
    return '成功打开网站：{}'.format(req.url)

@router_quick.post('/open-folder-by-vscode')
def open_folder_by_vscode(req: DesksetReqFolder):
    quick.open_folder_by_vscode(req.path)
    return '成功通过 vscode 打开文件夹：{}'.format(req.path)

@router_quick.get('/open-recycle')
def open_recycle():
    quick.open_recycle()
    return '成功打开回收站'
