from fastapi import APIRouter, Depends
from deskset.router.access import oauth2_scheme

from deskset.presenter.format import format_return
from deskset.feature.device import device

router_device = APIRouter(prefix='/v0/device', tags=['设备信息'], dependencies=[Depends(oauth2_scheme)])


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

# 电池信息
@router_device.get('/battery')
def get_battery():
    return format_return(device.battery())

# 系统信息
@router_device.get('/system')
def get_system():
    return format_return(device.system())
