import platform
import psutil
import threading
import time

from deskset.core.standard import DesksetError
from deskset.feature.device.abstract import AbstractDevice

ERR_GET_BATTERY_INFO = DesksetError(code=2001, message='无法获取电池信息')

# cpu_percent(interbal) 检测一次时间间隔
CPU_PERCENT_INTERVAL = 0


# 动态库
import ctypes
dll_disk_active_time = ctypes.windll.LoadLibrary('./lib/disk_active_time.dll')
dll_disk_active_time.start()
dll_disk_active_time.get.restype = ctypes.c_double


class Win32Device(AbstractDevice):
    def __init__(self, interval: float = 0.5):
        # 首次执行 psutil.cpu_percent() 结果可能为空（interval=0 时）
        # 所以初始化时提前执行一次，保证外部调用返回值有意义
        self.cpu()

        self.network = { 'sent': 0, 'recv': 0 }  # 单位 bytes/s

        self._interval = interval  # 轮询间隔 单位 s
        self._lock = threading.Lock()
        self._loop = threading.Thread(target=self.__loop_refresh)
        self._loop.daemon = True  # 守护线程，主进程结束时自动退出
        self._loop.start()

    def __loop_refresh(self) -> None:
        self.__last_net = psutil.net_io_counters()  # net 是 psutil 的 net，不是 self.network
        while True:
            time.sleep(self._interval)
            self._refresh_network()

    def cpu(self):
        """
        CPU：占用率 %</br>
        注：比任务管理器 CPU 占用率要略小一些，没啥好的解决办法（包括用 C）
        """
        return {
            "percent": psutil.cpu_percent(interval=CPU_PERCENT_INTERVAL)
        }

    def memory(self, is_format=True):
        memory = psutil.virtual_memory()

        if is_format:  # 格式化返回 GB
            return {
                "total": f'{((memory.total >> 20) / 1024):.1f}',
                "use":   f'{((memory.used  >> 20) / 1024):.1f}',
                "percent": memory.percent
            }

        return {
            "total":   memory.total,
            "use":     memory.used,
            "percent": memory.percent
        }

    def disk_useage(self):
        # 硬盘占用率 = 硬盘活动时间 = 1s 内读写所用时间 / 1s
        return round(dll_disk_active_time.get(), 1)

    def disk_partitions(self, is_format=True):
        """
        格式化：返回文件资源管理器显示的可用空间、总大小数据 free、total
        - 单位 Byte => GB，类型 int => str
        """
        partitions = []

        for partition in psutil.disk_partitions():
            partition_usage = psutil.disk_usage(partition.device)
            partitions.append({
                "root":    partition.device,
                "total":   partition_usage.total,
                "free":    partition_usage.free,
                "percent": partition_usage.percent
            })

        if is_format:
            def format_data(data):
                data = (data >> 20) / 1024

                if  100 <= data:
                    data = str(int(data))
                elif 10 <= data and data < 100:
                    data = int(data * 10) / 10
                    data = f'{data:.1f}'
                else:
                    data = int(data * 100) / 100
                    data = f'{data:.2f}'

                return data

            for partition in partitions:
                partition['total'] = format_data(partition['total'])
                partition['free']  = format_data(partition['free'])

        return partitions

    def _refresh_network(self) -> None:
        net = psutil.net_io_counters()

        self.network['sent'] = int((net.bytes_sent - self.__last_net.bytes_sent) / self._interval)
        self.network['recv'] = int((net.bytes_recv - self.__last_net.bytes_recv) / self._interval)

        self.__last_net = net

    def battery(self):
        battery = psutil.sensors_battery()

        # 设备可能没有电池：台式机、HTPC
        if battery is None:
            return ERR_GET_BATTERY_INFO

        return {
            "plug":    battery.power_plugged,
            "percent": battery.percent
        }

    def system(self):
        return {
            "name":    platform.node(),
            "system":  platform.system(),
            "version": platform.version(),
            "machine": platform.machine()
        }
