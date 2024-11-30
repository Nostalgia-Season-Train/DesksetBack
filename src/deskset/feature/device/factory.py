import platform

from deskset.feature.device.win32  import Win32Device
from deskset.feature.device.unknow import UnknowDevice


class DeviceFactory:
    _instance = None
    _device = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init') == False:
            self._is_init = True

    def get_device(self):
        if DeviceFactory._device is None:
            if platform.system() == "Windows":
                DeviceFactory._device = Win32Device()
            else:
                DeviceFactory._device = UnknowDevice()

        return DeviceFactory._device


device = DeviceFactory().get_device()
