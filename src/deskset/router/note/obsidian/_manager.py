from pathlib import Path

from deskset.feature.note.obsidian import *

class Manager(ConfVaultObserver):
    def __init__(self, conf_vault: ConfVault) -> None:
        conf_vault.attach(self)
        self.refresh(conf_vault)

    def update(self, conf_vault: ConfVault) -> None:
        self.refresh(conf_vault)

    def refresh(self, conf_vault: ConfVault) -> None:
        vault_path = conf_vault.path
        if not (Path(vault_path) / '.obsidian').is_dir():
            self.is_init = False
            return
        self.is_init = True
        self._vault_path = vault_path
        self.conf_noteapi = ConfNoteAPI(self._vault_path)
        self.conf_profile = ConfProfile(self._vault_path)

    @property
    def vault(self) -> str:
        return self._vault_path

conf_vault = ConfVault()
manager = Manager(conf_vault)


from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from deskset.router.unify import DesksetRepJSON
from deskset.router.unify import DesksetReqFolder

router_obsidian_manager = APIRouter(
    prefix='/obsidian-manager', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)

@router_obsidian_manager.get('/vault/get-path')
def get_vault_path():
    return conf_vault.path

@router_obsidian_manager.post('/vault/set-path')
def set_vault_path(req: DesksetReqFolder):
    conf_vault.path = req.path

# NoteAPI 通知 Back 自身状态：上线/下线
from ._noteapi import noteapi

@router_obsidian_manager.post('/noteapi/online')
async def noteapi_notify_online(
    address: str = Form(),
    token: str = Form(),
    vault: str = Form()
):
    return (await noteapi.set_online(address, token, vault))

@router_obsidian_manager.post('/noteapi/offline')
async def noteapi_notify_offline(address: str = Form(), token: str = Form()):
    return (await noteapi.set_offline(address, token))

# 通过流式响应，触发上下线事件
@router_obsidian_manager.get('/noteapi/event')
async def event():
    async def stream():
        await noteapi.online_status.wait()
        yield 'Online'
        await noteapi.offline_status.wait()
        yield 'Offline'
        return

    return StreamingResponse(stream(), media_type='text/plain')  # 加上 text/plain 这样 DevTools/网络/响应 才会显示文字

# 登入登出
  # 以下由于架构问题，无法实现
   # 注 1：独立处理登入登出的类。原因：登出需要 noteapi._token
   # 注 2：服务器关闭时，通过生命周期登出。原因：NoteAPI 登出会访问 /noteapi/offline，其在生命周期执行前关闭
from httpx import AsyncClient

from deskset.core.config import config
from deskset.router.unify.access import access

@router_obsidian_manager.post('/login-in')
async def login_in(
    address: str = Form('127.0.0.1:6528'),
    username: str = Form('noteapi-user'),
    password: str = Form('noteapi-pswd')
):
    async with AsyncClient() as client:
        response = await client.post(
            url=f'http://{address}/unify/login-in',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'username': username,
                'password': password,
                'backaddress': f'{config.server_host}:{config.server_port}',
                'backtoken': access.token
            }
        )

        if response.status_code != 200:
            from deskset.core.standard import DesksetError
            raise DesksetError(message=response.text)

        return response.text

@router_obsidian_manager.post('/login-out')
async def login_out():
    return (await noteapi.post(
        url='/unify/login-out',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'backaddress': f'{config.server_host}:{config.server_port}',
            'backtoken': access.token
        }
    )).text
