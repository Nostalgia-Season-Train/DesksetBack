# === Device ===
from deskset.core.standard import DesksetError

from deskset.feature.device import DeviceFactory

device = DeviceFactory.create_device()

def check_init() -> None:
    if device is None:
        raise DesksetError(code=2000, message='未知系统，无法读取设备信息')


# === 路由 ===
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token

from deskset.presenter.format import format_return

router_device = APIRouter(
    prefix='/v0/device', tags=['设备信息'],
    dependencies=[Depends(check_token), Depends(check_init)]
)


# CPU 信息
@router_device.get('/cpu')
def get_cpu():
    return format_return(device.cpu())

# 内存信息
@router_device.get('/memory')
def get_memory():
    return format_return(device.memory())

# 硬盘信息
@router_device.get('/disk')
def get_disk():
    return format_return(device.disk_partitions())

# 硬盘占用率（活动时间）
@router_device.get('/disk-useage')
def get_disk_useage():
    return format_return(device.disk_useage())

# 网络信息
@router_device.get('/network')
def get_network():
    return format_return(device.network)

# 电池信息
@router_device.get('/battery')
def get_battery():
    return format_return(device.battery())

# 系统信息
@router_device.get('/system')
def get_system():
    return format_return(device.system())

# SSE 返回消息
from asyncio import sleep, CancelledError
from asyncer import asyncify
from json import dumps
from sse_starlette.sse import EventSourceResponse

@router_device.get('/stream')
async def stream():
    async def get_device_info():
        try:
          while True:
                info = await asyncify(device.battery)()
                # 1、yield dict(data=ret) 而不是 yield ret（ret 代表返回值）
                # 2、sse 只能发送文本，字典后端序列化 json.dumps(dict) 前端反序列化 JSON.parse(str)
                  # 注：{ 'key': value } 不是 JSON 格式，key 没有带双引号
                yield { 'data': dumps(info) }
                await sleep(1)
        except CancelledError as cancel:
            pass
        finally:
            print('router_device/stream end sse')  # - [ ] 改成打印日志

    return EventSourceResponse(get_device_info())
