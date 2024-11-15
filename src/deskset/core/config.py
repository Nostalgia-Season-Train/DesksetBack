import os
from dynaconf import Dynaconf


class Setting(object):
    # obsidian 库的位置
    obsidian_vault = ''

    # obsidian 库的日记设置
    format = ''
    dir = ''
    template = ''

    def __new__(cls):
        if not hasattr(Setting, '_instance'):
            Setting._instance = object.__new__(cls)
        return Setting._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init'):
            return
        self.refresh()
        self._is_init = True

    def refresh(self):
        setting = Dynaconf(
            envvar_prefix = 'DYNACONF',
            settings_files = 'setting.json'
        )
        self.obsidian_vault = setting.get('obsidian_vault', default='')

        obsidian_config = Dynaconf(
            envvar_prefix = 'DYNACONF',
            settings_files = os.path.join(self.obsidian_vault, '.obsidian/daily-notes.json')
        )
        self.format = obsidian_config.get('format', default='YYYY-MM-DD')
        self.dir = os.path.join(self.obsidian_vault, obsidian_config.get('folder', default=''))
        self.template = obsidian_config.get('template', default='')
        # 临时解决方案：属性存在但值为空时 Dynaconf 不配置默认参数
        if self.format == '':
            self.format = 'YYYY-MM-DD'


setting = Setting()
