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
        ):
        self.code    = code
        self.message = message
        self.data    = data

@dataclass
class DesksetReturn():
    success: bool = False
    code:    int  = -1
    message: str  = _t('Not Sure Success Or Failure')
    data:    Any  = None
