from fastapi import APIRouter

from deskset.presenter.format import format_return
from deskset.feature.device import device

router_device = APIRouter(prefix='/device', tags=['设备信息'])


# CPU 信息
@router_device.get('/cpu')
async def get_cpu():
    return format_return(device.cpu)

# 内存信息
@router_device.get('/memory')
async def get_memory():
    return format_return(device.memory)

# 硬盘信息
@router_device.get('/disk_partitions')
async def get_disk_partitions():
    return format_return(device.disk_partitions)

# 电池信息
@router_device.get('/battery')
async def get_battery():
    return format_return(device.battery)

# 系统信息
@router_device.get('/system')
async def get_system():
    return format_return(device.system)
