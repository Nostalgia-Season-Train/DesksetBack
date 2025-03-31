# ==== 数字桌搭在笔记仓库中存放的配置 ====
  # 方便与仓库集成，不用切换仓库时切换配置
from typing import Optional
from pathlib import Path

from deskset.core.log import logging
from deskset.core.standard import DesksetError
from deskset.core.config import write_conf_file_abspath, read_conf_file_abspath

from deskset.feature.conf_app import ConfApp, ConfAppObserver, conf_app


# === 定期任务 ===
class VaultConfDesksetPeriodTask(ConfAppObserver):
    _confitem_tasks: Optional[list[dict]]

    def __init__(self, conf_app: ConfApp) -> None:
        conf_app.attach(self)
        self.refresh(conf_app.obsidian_vault)

    def update(self, conf_app: ConfApp) -> None:
        if self.vault != conf_app.obsidian_vault:
            self.refresh(conf_app.obsidian_vault)

    def refresh(self, vault_path: str) -> None:
        if (Path(vault_path) / '.obsidian').is_dir() == False:
            self.is_init = False
            self.vault = vault_path
            logging.error(f'Failed to set VaultConfDeskset, {vault_path} not a vault')
            return
        else:
            self.is_init = True
            self.vault = vault_path

        self._confabspath = str(Path(conf_app.obsidian_vault) / '.deskset' / 'period-task.yaml')
        self._confitem_tasks = [{ 'period': 'day', 'task': '演示每日任务' }]
        try:
            read_conf_file_abspath(self)
        except DesksetError as err:
            logging.error(err.message)
        finally:
            write_conf_file_abspath(self)


vault_conf_deskset_period_task = VaultConfDesksetPeriodTask(conf_app)
