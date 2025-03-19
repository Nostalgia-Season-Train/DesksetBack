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
from deskset.router.access import check_token

router_profile = APIRouter(
    prefix='/v0/profile',
    tags=['个人信息'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetResponse
)

@router_profile.get('/name')
def get_user_name():
    return '数字桌搭'
