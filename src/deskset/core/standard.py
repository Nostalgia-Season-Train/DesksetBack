from dataclasses import dataclass
from typing import Any

@dataclass
class DesksetSuccess():
    code: int = 0
    message: str = '成功'
    data: Any = None

@dataclass
class DesksetError():
    code: int = 1
    message: str = '失败'
    data: Any = None

@dataclass
class DesksetReturn():
    success: bool = False
    code: int = -1
    message: str = '不能确定正确与否！'
    data: Any = None
