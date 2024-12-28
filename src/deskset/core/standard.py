# 错误
from dataclasses import dataclass
from typing import Any

from deskset.core.locale import _t

@dataclass
class DesksetSuccess():
    code:    int = 0
    message: str = _t('Success')
    data:    Any = None

class DesksetError(Exception):
    def __init__(
            self,
            code:    int = 1,
            message: str = _t('Failure'),
            data:    Any = None
        ) -> None:
        self.code    = code
        self.message = message
        self.data    = data

    def insert(self, *args: str) -> Exception:
        """动态注释：注释初值包含占位符 {}，抛出异常时，动态插入错误信息"""
        # 1、初值
        #   yaml 文件：'This is a placeholder: {}': '这是一个占位符：{}'
        #   _t() 翻译：'This is a placeholder: {}'=>'这是一个占位符：{}'
        # 2、插入
        #   '这是一个占位符：{}'.format('dynamic') => '这是一个占位符：dynamic'
        #   注：对 self.message 中 {} 插入替换，因此 *arg 可以包含 {}
        try:
            return DesksetError(code=self.code, message=self.message.format(*args))
        except IndexError:  # 翻译前或翻译后，当占位符 {} 多于参数 args 时报错
            log_error = ''
            log_error += _t('DesksetError Dynamic Message! Extra Placeholder: ')
            log_error += f'\'{self.message}\'.format{args}'
            logging.error(log_error)

@dataclass
class DesksetReturn():
    success: bool = False
    code:    int  = -1
    message: str  = _t('Not Sure Success Or Failure')
    data:    Any  = None


# 日志
import logging

from deskset.core.config import config

logging.basicConfig(filename='log/latest.log', filemode='w', encoding=config.encoding)
