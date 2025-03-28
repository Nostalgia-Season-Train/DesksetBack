# === 输入验证 ===
from pydantic import BaseModel, field_validator

import os
from deskset.core.standard import DesksetError

class RequestFolder(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_folder(cls, v: str) -> str:
        if not os.path.isdir(v):
            raise DesksetError(message=f'错误！{v} 不是文件夹！')
        return v

class RequestApp(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_app(cls, v: str) -> str:
        # Linux 下可执行文件没有后缀，需要其他检查手段
        if os.path.isfile(v) != True or os.path.splitext(v)[1] != '.exe':
            raise DesksetError(message=f'错误！{v} 不是应用！')
        return v

class RequestWeb(BaseModel):
    url: str

class RequestScript(BaseModel):
    relpath: str  # 相对 DesksetBack.exe

    @field_validator('relpath')
    @classmethod
    def check_script(cls, v: str) -> str:
        abspath = os.path.join(os.getcwd(), 'script', f'{v}.py')
        if os.path.isfile(abspath) != True:
            raise DesksetError(message=f'错误！{abspath} 脚本不存在！')
        return v


# === 路由 ===
from fastapi import APIRouter, Depends
from deskset.router.access import check_token

from deskset.presenter.format import format_return

import deskset.feature.quick as quick
import deskset.feature.app.vscode as app_vscode

router_quick = APIRouter(prefix='/v0/quick', tags=['快速启动'], dependencies=[Depends(check_token)])

@router_quick.get('/open-default/{path:path}')
def open_default(path: str):
    if os.path.isfile(path) != True and os.path.isdir(path) != True:
        raise DesksetError(message=f'错误！路径 {path} 不存在！')
    return format_return(quick.open_default(path))

@router_quick.post('/open-app-through-path')
def open_app_through_path(req: RequestApp):
    quick.open_app_by_path(req.path)
    return format_return('成功打开应用：{}'.format(req.path))

@router_quick.post('/open-web-through-url')
def open_web_through_url(req: RequestWeb):
    quick.open_web_by_url(req.url)
    return format_return('成功打开网站：{}'.format(req.url))

@router_quick.post('/open-folder-by-vscode')
def open_folder_by_vscode(req: RequestFolder):
    app_vscode.open_folder_by_vscode(req.path)
    return format_return('成功通过 vscode 打开文件夹：{}'.format(req.path))

@router_quick.get('/open-recycle')
def open_recycle():
    quick.open_recycle()
    return format_return('成功打开回收站')

@router_quick.post('/execute-script')
def execute_script(req: RequestScript):
    quick.execute_script(req.relpath)
    return format_return('成功执行脚本')  # 后面加上返回值
