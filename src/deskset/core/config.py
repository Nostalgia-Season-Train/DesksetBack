from __future__ import annotations

import json

from deskset.core.log import logging

CONFIG_MAIN_PATH = './config/deskset.json'
CONFIG_MAIN_ENCODE = 'utf-8'


class Config(object):
    _instance: Config = None

    def __new__(cls) -> Config:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self._instance, '_is_init'):
            self._is_init = True
            self._init_once()

    def _init_once(self) -> None:
        # 1、属性设为默认值
        # 2、读取，检查通过后修改属性
        # 3、写入，属性覆盖上一步无效配置
        # 注意！不要添加跟配置无关的公有成员属性，此类依靠自身属性读取 json 配置

        # === 默认值 ===
        # 语言和编码
        self.language: str = 'zh-cn'
        self.encoding: str = 'utf-8'
        # 端口
        self.server_port: int = 8000
        # 用户和密码
        self.username: str = 'deskset-username'
        self.password: str = 'deskset-password'

        # === 读取 ===
        try:
            with open(CONFIG_MAIN_PATH, 'r', encoding=CONFIG_MAIN_ENCODE) as file:
                data: dict = json.load(file)

                for attr_key, attr_value in list(self.__dict__.items()):  # list 创建副本后修改 self 属性
                    # 不是私有成员属性
                    if attr_key.startswith('_'):
                        continue

                    # 配置类型跟默认值一致
                    config_key = attr_key.replace('_', '-')
                    config_type = type(attr_value)
                    if type(data.get(config_key)) != config_type:
                        continue

                    # 修改属性。注：setattr 可能丢掉类型检查
                    value = data.get(config_key)
                    if   config_type == type(10000):
                        setattr(self, attr_key, value)
                    elif config_type == type('str') and value != '':
                        setattr(self, attr_key, value)
                    else:
                        pass
        except FileNotFoundError:
            logging.warning(f'{CONFIG_MAIN_PATH} not found')
            pass
        except json.JSONDecodeError:
            logging.warning(f'{CONFIG_MAIN_PATH} decode failed')
            pass

        # === 写入 ===
        with open(CONFIG_MAIN_PATH, 'w', encoding=CONFIG_MAIN_ENCODE) as file:
            data: dict = {
                key.replace('_', '-'): value for key, value in self.__dict__.items() if not key.startswith('_')
            }
            json.dump(data, file, ensure_ascii=False, indent=4)


config = Config()


if __name__ == '__main__':
    for attr_key, attr_value in config.__dict__.items():
        print(attr_key, attr_value)
