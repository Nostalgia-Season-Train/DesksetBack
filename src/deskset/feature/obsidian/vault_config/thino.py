import json
from pathlib import Path

from deskset.core.config import config


class ConfigVaultPlugin:
    def __init__(self, vault_path: str) -> None:
        self.vault_path = Path(vault_path)

        # Thino（原 Memos）选项
        self.activity_heading = '# 动态'
        self.activity_format  = 'HH:mm:ss'
        try:
            conf_path = self.vault_path / '.obsidian/plugins/obsidian-memos/data.json'
            with open(file=conf_path, mode='r', encoding=config.encoding) as conf_file:
                conf: dict = json.load(conf_file)
                if conf.get('ProcessEntriesBelow') != None and conf.get('ProcessEntriesBelow') != '':
                    self.activity_heading = conf.get('ProcessEntriesBelow')
                if conf.get('DefaultTimePrefix') != None and conf.get('DefaultTimePrefix') != '':
                    self.activity_format = conf.get('DefaultTimePrefix')
        except FileNotFoundError:
            pass
