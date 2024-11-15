# 获取并返回硬件系统信息
# 返回单位：字节 Byte、百分比 %

import psutil
import platform

from deskset.core.standard import DesksetError

# 检查 CPU 占用率所用间隔
# 原本为 0 时，第一次执行 cpu() 的返回值为空无意义
# 但是类在初始化时会执行一次 cpu()
# 所以在外部第一次调用 cpu() 方法时不为零（实际上是第二次执行）
CPU_PERCENT_INTERVAL = 0

ERR_GET_BATTERY_INFO = DesksetError(code=2000, message='无法获取电池信息')


class Device:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init') == False:
            self._is_init = True

            self._cpu = self.cpu()
            self._memory = self.memory()
            self._disk_partitions = self.disk_partitions()
            self._battery = self.battery()
            self._system = self.system()

    # CPU：占用率
    def cpu(self):
        return {
            "percent": psutil.cpu_percent(interval=CPU_PERCENT_INTERVAL)
        }

    # 内存：容量、使用、占用率
    def memory(self):
        memory = psutil.virtual_memory()

        return {
            "total": memory.total,
            "use": memory.used,
            "percent": memory.percent
        }

    # 硬盘分区：根路径、容量、使用、占用率
    def disk_partitions(self):
        partitions = []

        for partition in psutil.disk_partitions():
            partition_usage = psutil.disk_usage(partition.device)
            partitions.append({
                "root": partition.device,
                "total": partition_usage.total,
                "use": partition_usage.used,
                "percent": partition_usage.percent
            })

        return partitions

    # 电池：是否充电、剩余电量百分比
    def battery(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return ERR_GET_BATTERY_INFO
        else:
            return {
                "plug": battery.power_plugged,
                "percent": battery.percent
            }

    # 系统：系统类型、系统版本、设备名称、芯片架构
    def system(self):
        return {
            "name": platform.node(),
            "system": platform.system(),
            "version": platform.version(),
            "machine": platform.machine()
        }


device = Device()
