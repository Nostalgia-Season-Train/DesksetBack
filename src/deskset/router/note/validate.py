from pydantic import BaseModel, field_validator
import arrow

from deskset.core.standard import DesksetError

class DesksetReqDateDay(BaseModel):
    day: str  # 某天，日期格式：YYYYMMDD，比如 20250324

    @field_validator('day')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMMDD')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！某天 {v} 日期格式有误！应为 YYYYMMDD')

class DesksetReqDateMonth(BaseModel):
    month: str  # 某月，日期格式：YYYYMM，比如 202503

    @field_validator('month')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMM')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！某月 {v} 日期格式有误！应为 YYYYMM')
