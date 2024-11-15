from dataclasses import asdict

from ..core.standard import *


def format_return(old_func):
    """
    格式化返回值
    """
    async def new_func():
        result = await old_func()

        if type(result) == DesksetError:
            return asdict(DesksetReturn(
                success=False,
                code=result.code,
                message=result.message
            ))
        else:
            return asdict(DesksetReturn(
                success=True,
                data=result
            ))

    return new_func
