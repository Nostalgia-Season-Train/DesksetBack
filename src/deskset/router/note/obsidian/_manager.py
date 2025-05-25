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

from fastapi import WebSocket, WebSocketDisconnect
from ._noteapi import noteapi

@router_obsidian_manager.websocket('/ws-event')
async def ws_event(websocket: WebSocket):
    await websocket.accept()

    try:
        # 首次传输：初始化
        noteapi_info = await websocket.receive_json()

        address = noteapi_info['address']
        token = noteapi_info['token']
        path = noteapi_info['path']
        setting = noteapi_info['setting']

        await noteapi.set_online(address, token, path, setting, websocket)

        # 后续传输：Obsidian 消息事件
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        pass
    finally:
        await noteapi.set_offline(address, token)
