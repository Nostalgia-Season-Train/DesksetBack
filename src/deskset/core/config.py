from __future__ import annotations
from typing import Optional

# 为了在 config 目录区分 DesksetBack 和 DesksetFront 配置
import yaml  # DesksetBack 优先配置格式 yaml
import json  # DesksetFront 优先配置格式 json

from deskset.core.log import logging

CONFIG_MAIN_PATH = './config/desksetback.yaml'
CONFIG_MAIN_ENCODE = 'utf-8'


# ==== 读写 config/desksetback.yaml 中的配置 ====
class Config:
    def __init__(self) -> None:
        # --- 1、设置默认值 ---
        # 语言和编码
        self._confitem_language: str = 'zh-cn'
        self._confitem_encoding: str = 'utf-8'
        # 端口
        self._confitem_server_host: str = '127.0.0.1'
        self._confitem_server_port: int = 6527
        # 用户和密码：self.username 和 self.password 每次都随机生成，读取配置文件成功再被覆盖
        import random
        import string
        letters_and_digits = string.ascii_letters + string.digits
        self._confitem_username: str = 'deskset-user' + ''.join(random.choices(letters_and_digits, k=random.randint(5, 10)))
        self._confitem_password: str = 'deskset-pswd' + ''.join(random.choices(letters_and_digits, k=random.randint(10, 20)))

        # --- 2、先读再写，覆盖无效配置项 ---
        self._read_config_file()
        self._write_config_file()

    def _read_config_file(self) -> None:
        try:
            with open(CONFIG_MAIN_PATH, 'r', encoding=CONFIG_MAIN_ENCODE) as file:
                data: dict = yaml.safe_load(file)

                for attr_key, attr_value in list(self.__dict__.items()):  # list 创建副本后修改 self 属性
                    if not attr_key.startswith('_confitem_'):
                        continue

                    # 配置类型跟默认值一致
                    config_key = attr_key[10:].replace('_', '-')
                    config_type = type(attr_value)
                    if type(data.get(config_key)) != config_type:
                        continue

                    # 修改属性。注：setattr 不会丢掉类型检查
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
        except yaml.YAMLError:
            logging.warning(f'{CONFIG_MAIN_PATH} decode failed')
            pass

    def _write_config_file(self, yaml_key: str | None = None, yaml_value: object | None = None) -> None:
        with open(CONFIG_MAIN_PATH, 'w', encoding=CONFIG_MAIN_ENCODE) as file:
            data: dict = {
                key[10:].replace('_', '-'): value for key, value in self.__dict__.items() if key.startswith('_confitem_')
            }
            # 先写入文件，再修改属性
            if yaml_key is not None and yaml_value is not None and data.get(yaml_key, None) is not None:
                if type(data[yaml_key]) == type(yaml_value):
                    data[yaml_key] = yaml_value
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)
                setattr(self, '_confitem_' + yaml_key.replace('-', '_'), yaml_value)
            # 直接写入文件
            else:
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)

    @property
    def language(self) -> str:
        return self._confitem_language

    @property
    def encoding(self) -> str:
        return self._confitem_encoding

    @property
    def server_host(self) -> str:
        return self._confitem_server_host

    @property
    def server_port(self) -> int:
        return self._confitem_server_port

    @property
    def username(self) -> str:
        return self._confitem_username

    @username.setter
    def username(self, username: str) -> None:
        if len(username) == 0:
            raise ValueError('username cannot be empty string')
        self._write_config_file('username', username)

    @property
    def password(self) -> str:
        return self._confitem_password

    @password.setter
    def password(self, password: str) -> None:
        if len(password) == 0:
            raise ValueError('password cannot be empty string')
        self._write_config_file('password', password)


config = Config()


if __name__ == '__main__':
    for attr_key, attr_value in config.__dict__.items():
        print(attr_key, attr_value)


# ==== 配置读写函数 ====
  # 根据实例成员，读写配置
  # _confpath 以 config 作根目录，读写 config/{_confpath}.yaml 文件，编码一律 utf-8
  # _confitem_key = value 对应 key: value 配置项
    # _confitem_custom_prop 下划线将被连字符替换 custom-prop
  # 使用提醒：
    # 成员：self._confXXX（注意 self）
    # 类型提示：class Conf: _confXXX: str（在类中注解）
from pathlib import Path
from typing import get_type_hints, get_args

# 这里存在循环引用 config < standard < locale < config
  # 但是只要 config 在此之前定义，那就没有问题
from deskset.core.standard import DesksetError

READ_CONFFILE_ERROR = DesksetError(message='配置文件 {} 读取失败：{}！')


def write_conf_file(instance: object) -> None:
    if getattr(instance, '_confpath', None) is None:
        raise ValueError(f'_confpath not exist in {type(instance)} class')
    relpath = Path('./config') / f'{instance._confpath}.yaml'  # type: ignore

    items = {}  # 配置项

    for attr_key, attr_value in list(instance.__dict__.items()):
        if not attr_key.startswith('_confitem_'):
            continue

        key = attr_key[len('_confitem_'):].replace('_', '-')  # [len('_confitem_'):] 去掉 _confitem_
        value = attr_value
        items[key] = value  # Python 3.7+ 开始字典有序

    relpath.parent.mkdir(parents=True, exist_ok=True)  # open 不会创建目录，用 Path 提前创建

    with open(relpath, 'w', encoding='utf-8') as file:
        yaml.dump(items, file, allow_unicode=True, sort_keys=False)  # sort_keys=False 不排序


def read_conf_file(instance: object) -> None:
    if getattr(instance, '_confpath', None) is None:
        raise ValueError(f'_confpath not exist in {type(instance)} class')
    relpath = Path('./config') / f'{instance._confpath}.yaml'  # type: ignore

    # 读取文件，异常由调用方处理
      # 可能异常：文件不存在 FileNotFoundError、yaml 解析失败 yaml.YAMLError、yaml 解析非字典 TypeError
    if not relpath.is_file():
        raise READ_CONFFILE_ERROR.insert(str(relpath), '文件不存在')
    with open(relpath, 'r', encoding='utf-8') as file:
        try:
            items: dict = yaml.safe_load(file)
        except yaml.YAMLError:
            raise READ_CONFFILE_ERROR.insert(str(relpath), 'YAML 解析失败')

        # 没解析成字典，也算异常
        if not isinstance(items, dict):
            raise READ_CONFFILE_ERROR.insert(relpath, '解析结果不是字典')

        # attr_value 作为配置项默认值
        for attr_key, attr_value in list(instance.__dict__.items()):
            if not attr_key.startswith('_confitem_'):
                continue

            value_type = type(attr_value)
            key = attr_key[len('_confitem_'):].replace('_', '-')
            value = items.get(key, None)

            if type(value) != value_type:  # 值类型 != 配置项默认值类型
                continue

            if   value_type == type(10000):
                setattr(instance, attr_key, value)
            elif value_type == type('str'):
                if value != '':
                    setattr(instance, attr_key, value)
                if value == '':  # 类型标注包含 None = 允许空字符串
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, '')


# ==== 配置读写函数（绝对路径） ====
  # 配置路径从绝对路径 _confabspath（包括文件后缀）读取
def write_conf_file_abspath(instance: object, format: str = 'yaml') -> None:
    if getattr(instance, '_confabspath', None) is None:
        raise ValueError(f'_confabspath not exist in {type(instance)} class')
    abspath = Path(instance._confabspath)  # type: ignore

    items = {}  # 配置项

    for attr_key, attr_value in list(instance.__dict__.items()):
        if not attr_key.startswith('_confitem_'):
            continue

        key = attr_key[len('_confitem_'):].replace('_', '-')  # [len('_confitem_'):] 去掉 _confitem_
        value = attr_value
        items[key] = value  # Python 3.7+ 开始字典有序

    abspath.parent.mkdir(parents=True, exist_ok=True)  # open 不会创建目录，用 Path 提前创建

    with open(abspath, 'w', encoding='utf-8') as file:
        if format == 'yaml':
            yaml.dump(items, file, allow_unicode=True, sort_keys=False)  # sort_keys=False 不排序
        if format == 'json':
            json.dump(items, file, ensure_ascii=False, indent=4)


def read_conf_file_abspath(instance: object, format: str = 'yaml') -> None:
    if getattr(instance, '_confabspath', None) is None:
        raise ValueError(f'_confabspath not exist in {type(instance)} class')
    abspath = Path(instance._confabspath)  # type: ignore

    # 读取文件，异常由调用方处理
      # 可能异常：文件不存在 FileNotFoundError、yaml 解析失败 yaml.YAMLError、yaml 解析非字典 TypeError
    if not abspath.is_file():
        raise READ_CONFFILE_ERROR.insert(str(abspath), '文件不存在')
    with open(abspath, 'r', encoding='utf-8') as file:
        if format == 'yaml':
            try:
                items: dict = yaml.safe_load(file)
            except yaml.YAMLError:
                raise READ_CONFFILE_ERROR.insert(str(abspath), 'YAML 解析失败')
        if format == 'json':
            try:
                items: dict = json.load(file)
            except json.JSONDecodeError:
                raise READ_CONFFILE_ERROR.insert(str(abspath), 'JSON 解析失败')

        # 没解析成字典，也算异常
        if not isinstance(items, dict):  # type: ignore 暂时不管...
            raise READ_CONFFILE_ERROR.insert(str(abspath), '解析结果不是字典')

        # attr_value 作为配置项默认值
        for attr_key, attr_value in list(instance.__dict__.items()):
            if not attr_key.startswith('_confitem_'):
                continue

            value_type = type(attr_value)
            key = attr_key[len('_confitem_'):].replace('_', '-')
            value = items.get(key, None)

            if type(value) != value_type:  # 值类型 != 配置项默认值类型
                continue

            if   value_type == type(10000):
                setattr(instance, attr_key, value)
            elif value_type == type('str'):
                if value != '':
                    setattr(instance, attr_key, value)
                if value == '':  # 类型标注包含 None = 允许空字符串
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, '')
            elif value_type == type([]):  # 附：可以解析 list[dict] 类型
                if len(value) != 0:  # type: ignore vscode pyright 无法间接推断 value 类型
                    setattr(instance, attr_key, value)
                if len(value) == 0:  # 同上，包含 None 允许列表为空  # type: ignore 同上
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, [])
