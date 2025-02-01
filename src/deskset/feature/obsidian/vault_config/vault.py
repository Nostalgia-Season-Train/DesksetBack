import json
from pathlib import Path

from deskset.core.config import config


class ConfigVault:
    def __init__(self, vault_path: str) -> None:
        self.vault_path = Path(vault_path)

        # 日记选项
        self.diary_format   = 'YYYY-MM-DD'
        self.diary_folder   = ''
        self.diary_template = ''
        try:
            conf_path = self.vault_path / '.obsidian/daily-notes.json'
            with open(file=conf_path, mode='r', encoding=config.encoding) as conf_file:
                conf: dict = json.load(conf_file)
                if conf.get('format') != None and conf.get('format') != '':
                    self.diary_format = conf.get('format')
                if conf.get('folder')   is not None: self.diary_folder   = conf.get('folder')
                if conf.get('template') is not None: self.diary_template = conf.get('template')
        except FileNotFoundError:
            pass
