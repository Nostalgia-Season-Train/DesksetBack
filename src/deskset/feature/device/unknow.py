from deskset.core.standard import DesksetError
from deskset.feature.device.abstract import AbstractDevice

ERR_UNKNOW_DEVICE = DesksetError(code=2000, message='未知系统，无法读取设备信息')


class UnknowDevice(AbstractDevice):
    def cpu(self):
        return ERR_UNKNOW_DEVICE

    def memory(self):
        return ERR_UNKNOW_DEVICE

    def disk_partitions(self):
        return ERR_UNKNOW_DEVICE

    def battery(self):
        return ERR_UNKNOW_DEVICE

    def system(self):
        return ERR_UNKNOW_DEVICE
