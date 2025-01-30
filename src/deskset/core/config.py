from pathlib import Path
from dynaconf import Dynaconf

CONFIG_MAIN = './config/app-back.json'  # 主要配置文件的路径


class Config(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self._instance, '_is_init'):
            self._is_init = True

            self.refresh()

    def refresh(self):
        # 读取设置
        self._setting = Dynaconf(
            envvar_prefix  = 'DYNACONF',
            settings_files = CONFIG_MAIN
        )

        # 语言：默认 中文
        # 编码：默认 UTF-8
        self.language = self._setting.get('language', default='zh-cn')
        self.encoding = self._setting.get('encoding', default='utf-8')

        # Obsidian：obsidian 库的位置
        self.obsidian_vault = self._setting.get('obsidian_vault', default='')

        # obsidian 库的日记设置
        obsidian_config = Dynaconf(
            envvar_prefix  = 'DYNACONF',
            settings_files = str(Path(self.obsidian_vault) / '.obsidian/daily-notes.json')
        )
        self.format   = obsidian_config.get('format'  , default='YYYY-MM-DD')
        self.dir      = str(Path(self.obsidian_vault) / obsidian_config.get('folder', default=''))
        self.template = obsidian_config.get('template', default='')
        # 临时解决方案：属性存在但值为空时 Dynaconf 不配置默认参数
        if self.format == '':
            self.format = 'YYYY-MM-DD'


config = Config()
