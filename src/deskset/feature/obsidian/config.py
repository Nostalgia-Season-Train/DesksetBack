from dynaconf import Dynaconf

CONFIG_OBSIDIAN = './config/app/obsidian.yaml'


class ConfigAppObsidian:
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
        self._setting = Dynaconf(
            envvar_prefix  = 'DYNACONF',
            settings_files = CONFIG_OBSIDIAN
        )

        # Obsidian 仓库位置
        self.obsidian_vault = self._setting.get('obsidian_vault', default='')


config_app_obsidian = ConfigAppObsidian()
