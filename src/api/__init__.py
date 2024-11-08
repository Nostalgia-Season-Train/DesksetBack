from dataclasses import dataclass, asdict
from typing import Any

SUCCESS = 0
SUCCESS_INFO = '成功'


@dataclass
class Success():
    code: int = 0
    message: str = '成功'

@dataclass
class Error():
    code: int
    message: str

@dataclass
class DDSReturn():
    success: bool
    code: int
    message: str
    data: Any = None


# ===== 分割线 =====


# 待定：返回调用修改建议
ERROR_STRUCT = Error(code='1000', message='调用结构错误！')
ERROR_FUNC = Error(code='1001', message='无此函数！')
ERROR_PARAM = Error(code='1002', message='传参错误！')


def DSS_exchange(obj: object, call: dict):
    """
    输入：obj 对象，call 调用
    """
    try:
        result = getattr(obj, call['func'])(**call['param'])
        if type(result) == Error:
            return asdict(DDSReturn(
                success=False,
                code=result.code,
                message=result.message
            ))
        else:
            return asdict(DDSReturn(
                success=True,
                code=SUCCESS,
                message=SUCCESS_INFO,
                data=result
            ))
    except KeyError:
        return asdict(DDSReturn(
            success=False,
            code=ERROR_STRUCT.code,
            message=ERROR_STRUCT.message,
            data=call
        ))
    except AttributeError:
            return asdict(DDSReturn(
                success=False,
                code=ERROR_FUNC.code,
                message=ERROR_FUNC.message,
                data=call
            ))
    except TypeError:
        return asdict(DDSReturn(
                success=False,
                code=ERROR_PARAM.code,
                message=ERROR_PARAM.message,
                data=call
            ))
