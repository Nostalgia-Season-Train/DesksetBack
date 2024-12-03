from dataclasses import dataclass
from typing import Any

@dataclass
class DesksetSuccess():
    code:    int = 0
    message: str = 'Success'
    data:    Any = None

class DesksetError(Exception):
    def __init__(
            self,
            code:    int = 1,
            message: str = 'Failure',
            data:    Any = None
        ):
        self.code    = code
        self.message = message
        self.data    = data

@dataclass
class DesksetReturn():
    success: bool = False
    code:    int  = -1
    message: str  = 'Not Sure Success Or Failure'
    data:    Any  = None
