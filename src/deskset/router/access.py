from fastapi import APIRouter

router_access = APIRouter(prefix='/v0/access', tags=['认证'])


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v0/access/login')  # tokenUrl 写全 URL

@router_access.post('/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
    # 输入和输出：username、password，access_token、token_type 都不需要自己指定键名
    if form.username != 'deskset-username':
        raise HTTPException(status_code=400, detail='无效用户')
    if form.password != 'deskset-password':
        raise HTTPException(status_code=400, detail='无效密码')

    return {
        'access_token': 'deskset-token',
        'token_type': 'bearer'
    }

@router_access.get('/user-info')
def user_info(token: str = Depends(oauth2_scheme)):
    return token
