from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from ._manager import api as noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/active-file')
async def get_active_file():
    async def stream():
        # 初始化
        yield await noteapi.get_active_file()
        # 轮询等待 active-leaf-change 事件
        while True:
            await noteapi.event_active_leaf_change()
            if noteapi.is_offline:
                break  # 判断 event_active_leaf_change 是否由下线触发
            yield await noteapi.get_active_file()
        return

    return StreamingResponse(stream(), media_type='text/plain')
