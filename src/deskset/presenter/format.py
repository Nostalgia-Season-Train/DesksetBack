from dataclasses import asdict

from deskset.core.standard import *


def format_return(func):
    """
    格式化返回值
    """
    result = func()

    if type(result) == DesksetError:
        return asdict(DesksetReturn(
            success=False,
            code=result.code,
            message=result.message,
            data=DesksetError.data
        ))
    else:
        return asdict(DesksetReturn(
            success=True,
            code=DesksetSuccess.code,
            message=DesksetSuccess.message,
            data=result
        ))
