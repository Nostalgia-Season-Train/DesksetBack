from __future__ import annotations
from typing import Optional

import json

from deskset.core.log import logging

CONFIG_MAIN_PATH = './config/deskset.json'
CONFIG_MAIN_ENCODE = 'utf-8'


# ==== 读取 config/deskset.json 中的配置 ====
  # - [ ] 需要换名 + 移至其他文件
class Config(object):
    _instance: Optional[Config] = None

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
        self.server_port: int = 6527
        # 用户和密码：self.username 和 self.password 每次都随机生成，读取配置文件成功再被覆盖
        import random
        import string
        letters_and_digits = string.ascii_letters + string.digits
        self.username: str = 'deskset-user' + ''.join(random.choices(letters_and_digits, k=random.randint(5, 10)))
        self.password: str = 'deskset-pswd' + ''.join(random.choices(letters_and_digits, k=random.randint(10, 20)))

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


# ==== 配置读写函数 ====
  # 根据实例成员，读写配置
  # _conf_relpath 以 config 作根目录，读写 config/{_conf_relpath}.yaml 文件，编码一律 utf-8
  # _item_key = value 对应 key: value 配置项
    # _item_custom_prop 下划线将被连字符替换 custom-prop
from pathlib import Path

import yaml

def write_conf_file(instance: object):
    if getattr(instance, '_conf_relpath', None) is None:
        raise ValueError(f'_conf_relpath not exist in {type(instance)} class')
    relpath = Path('./config') / f'{instance._conf_relpath}.yaml'

    items = {}  # 配置项

    for attr_key, attr_value in list(instance.__dict__.items()):
        if not attr_key.startswith('_item_'):
            continue

        key = attr_key[6:].replace('_', '-')  # [6:] 去掉 _item_
        value = attr_value
        items[key] = value  # Python 3.7+ 开始字典有序

    with open(relpath, 'w', encoding='utf-8') as file:
        yaml.dump(items, file, allow_unicode=True)
