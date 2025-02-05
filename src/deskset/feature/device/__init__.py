import platform

from deskset.feature.device.win32  import Win32Device
from deskset.feature.device.unknow import UnknowDevice


class DeviceFactory:
    _device = None

    @staticmethod
    def create_device():
        if DeviceFactory._device is None:
            if platform.system() == 'Windows':
                DeviceFactory._device = Win32Device()
            else:
                DeviceFactory._device = UnknowDevice()

        return DeviceFactory._device


device = DeviceFactory.create_device()
