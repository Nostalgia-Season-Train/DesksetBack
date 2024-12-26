import platform
import psutil

from deskset.core.standard import DesksetError
from deskset.feature.device.abstract import AbstractDevice

ERR_GET_BATTERY_INFO = DesksetError(code=2001, message='无法获取电池信息')

# cpu_percent(interbal) 检测一次时间间隔
CPU_PERCENT_INTERVAL = 0


class Win32Device(AbstractDevice):
    def __init__(self):
        # 首次执行 psutil.cpu_percent() 结果可能为空（interval=0 时）
        # 所以初始化时提前执行一次，保证外部调用返回值有意义
        self.cpu()

    def cpu(self):
        """
        CPU：占用率 %</br>
        注：比任务管理器 CPU 占用率要略小一些，没啥好的解决办法（包括用 C）
        """
        return {
            "percent": psutil.cpu_percent(interval=CPU_PERCENT_INTERVAL)
        }

    def memory(self):
        memory = psutil.virtual_memory()

        return {
            "total":   memory.total,
            "use":     memory.used,
            "percent": memory.percent
        }

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
