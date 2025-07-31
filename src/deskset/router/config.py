# ==== Router ====
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

router_config = APIRouter(
    prefix='/v0/config', tags=['配置'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


# ==== URL ====
from fastapi import Form
from deskset.core.config import config

@router_config.get('/username')
def get_username():
    return config.username

@router_config.post('/username')
def post_username(username: str = Form()):
    config.username = username

@router_config.get('/password')
def get_password():
    return config.password

@router_config.post('/password')
def post_password(password: str = Form()):
    config.password = password
