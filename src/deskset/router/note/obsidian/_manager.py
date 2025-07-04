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

# - [ ] 等待封装进 manager
wstoken = access._generate_token('username', 'password')

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
                'backtoken': wstoken
            }
        )

        if response.status_code != 200:
            from deskset.core.standard import DesksetError
            raise DesksetError(message=response.text)

        return response.text

from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from deskset.router.unify.access import access
from ._noteapi import noteapi

@router_obsidian_manager.websocket('/ws-event')
async def ws_event(websocket: WebSocket):
    async def is_authorized(subprotocols: list[str]):
        if len(subprotocols) != 2:
            return False
        if subprotocols[0] != 'Authorization':
            return False
        if subprotocols[1] != f'bearer-{wstoken}':
            return False
        return True

    if not await is_authorized(websocket.scope['subprotocols']):
        await access.add_fail_time_async()
        raise HTTPException(status_code=400, detail='无效密钥')
    await websocket.accept('Authorization')  # 前后端都要有 Authorization 子协议，否则无法建立连接

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

# - [ ] 临时：RPC 测试
from ._rpc import RpcClient

class API:
    _rpc: RpcClient | None

    async def helloworld(self) -> str:
        if self._rpc != None:
            return await self._rpc.call_remote_procedure('helloworld', [])
        else:
            return 'RPC 没有上线'

api = API()

@router_obsidian_manager.websocket('/rpc')
async def rpc(websocket: WebSocket):
    await websocket.accept()

    # 上线 > 轮询接收 > 下线
    api._rpc = RpcClient(websocket)

    try:
        while True:
            response = await websocket.receive_json()
            await api._rpc.on_receive(response)
    except WebSocketDisconnect:
        pass

    api._rpc = None

@router_obsidian_manager.get('/helloworld')
async def helloworld():
    return await api.helloworld()
