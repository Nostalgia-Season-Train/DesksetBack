from dynaconf import Dynaconf

CONFIG_MAIN = './config/deskset-back.json'


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


config = Config()
