from dataclasses import asdict

from deskset.core.standard import *


def format_return(result):
    """
    格式化返回值
    """
    if type(result) == DesksetError:
        return asdict(DesksetReturn(
            success = False,
            code    = result.code,
            message = result.message,
            data    = result.data
        ))
    else:
        return asdict(DesksetReturn(
            success = True,
            code    = DesksetSuccess.code,
            message = DesksetSuccess.message,
            data    = result
        ))
