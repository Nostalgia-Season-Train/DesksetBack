# === Device ===
from deskset.core.standard import DesksetError

from deskset.feature.device import DeviceFactory

device = DeviceFactory.create_device()

def check_init() -> None:
    if device is None:
        raise DesksetError(code=2000, message='未知系统，无法读取设备信息')


# === 路由 ===
from fastapi import APIRouter, Depends
from deskset.router.access import check_token

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
