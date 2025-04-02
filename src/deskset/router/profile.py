# ==== 配置 ====
from typing import Optional

from deskset.core.log import logging
from deskset.core.standard import DesksetError

from deskset.core.config import write_conf_file, read_conf_file

class ConfProfile:
    _confitem_name: str
    _confitem_bio: Optional[str]

    def __init__(self):
        self._confpath = 'profile/data'
        self._confitem_name = '数字桌搭'
        self._confitem_bio = '数字桌搭，桌面美化与笔记应用的完美互动'
        try:
            read_conf_file(self)
        except DesksetError as err:
            logging.error(err.message)
        finally:
            write_conf_file(self)


# ==== 响应 ====
from fastapi import Response
import orjson

class DesksetResponse(Response):
    media_type = 'application/json'

    def render(self, content: object) -> bytes:
        response = {
            'success': True,
            'code': 0,
            'message': 'Success',
            'result': content
        }
        return orjson.dumps(response)


# ==== 路由 ====
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token

router_profile = APIRouter(
    prefix='/v0/profile',
    tags=['个人信息'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetResponse
)

@router_profile.get('/name')
def get_user_name():
    profile = ConfProfile()  # 临时性的，方便测试
    return {
        'name': profile._confitem_name,
        'bio': profile._confitem_bio
    }
