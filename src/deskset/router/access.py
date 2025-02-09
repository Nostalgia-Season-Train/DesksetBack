# access 权限
from __future__ import annotations
from typing import Optional

from deskset.core.config import config

class Access(object):
    _instance: Optional[Access] = None

    def __new__(cls) -> Access:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self._instance, '_is_init'):
            self._is_init = True
            self._token: str = self._generate_token(config.username, config.password)

    def _generate_token(self, username: str, password: str) -> str:
        from datetime import datetime
        current: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        import os
        key: bytes = os.urandom(32)
        msg: bytes = (username + current + password).encode()

        import hmac
        import hashlib
        token: str = hmac.new(key, msg, hashlib.sha256).hexdigest()

        return token

    @property
    def token(self) -> str:
        return self._token

    def set_token(self, token: str) -> None:
        self._token = token

    def get_token(self) -> str:
        return self._token

access = Access()


# router 路由
from fastapi import APIRouter

router_access = APIRouter(prefix='/v0/access', tags=['认证'])


# oauth2_scheme 验证 token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v0/access/login')  # tokenUrl 写全 URL

def check_token(token: str = Depends(oauth2_scheme)) -> bool:  # Depends(oauth2_scheme) 拿取 request.token
    if token != access.token:
        raise HTTPException(status_code=400, detail='无效密钥')
    return True

@router_access.post('/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
    # 输入和输出：username、password，access_token、token_type 都不需要自己指定键名
    if form.username != config.username:
        raise HTTPException(status_code=400, detail='无效用户')
    if form.password != config.password:
        raise HTTPException(status_code=400, detail='无效密码')

    return {
        'access_token': access.token,
        'token_type': 'bearer'
    }

@router_access.get('/user-info')
def user_info(token: str = Depends(check_token)):
    return config.username
