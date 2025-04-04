from __future__ import annotations
from abc import ABC, abstractmethod

import yaml

CONF_APP_PATH = './config/app.yaml'


class ConfApp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self._instance, '_is_init'):
            self._is_init = True
            self._observers: list[ConfAppObserver] = []
            self._conf = {
                'obsidian_vault': ''
            }
            try:
                with open(CONF_APP_PATH, 'r', encoding='utf-8') as file:
                    conf: dict = yaml.safe_load(file)
                    if conf.get('obsidian_vault') is not None:
                        self._conf['obsidian_vault'] = conf.get('obsidian_vault')
            except FileNotFoundError:
                with open(CONF_APP_PATH, 'w', encoding='utf-8') as file:
                    yaml.dump(self._conf, file, allow_unicode=True)  # 只能用 utf-8

    def attach(self, observer: ConfAppObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: ConfAppObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        with open(CONF_APP_PATH, 'w', encoding='utf-8') as file:
            yaml.dump(self._conf, file, allow_unicode=True)
        # 后面加上，按类型选择性更新
        for observer in self._observers:
            observer.update(self)

    # obsidian_vault 属性
    @property
    def obsidian_vault(self) -> str:
        return self._conf['obsidian_vault']

    @obsidian_vault.setter
    def obsidian_vault(self, vault_path: str) -> None:
        self._conf['obsidian_vault'] = vault_path
        self.notify()

class ConfAppObserver(ABC):
    # ConfApp 是单例模式，所以传入的 subject 参数可以跟 conf_app 实例重名
    @abstractmethod
    def update(self, conf_app: ConfApp) -> None:
        pass


conf_app = ConfApp()
