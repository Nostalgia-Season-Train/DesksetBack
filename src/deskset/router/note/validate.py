from pydantic import BaseModel, field_validator
import arrow

from deskset.core.standard import DesksetError

class DesksetReqDate(BaseModel):
    date: str  # 日期格式：YYYYMMDD，比如 20250324

    @field_validator('date')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMMDD')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！日期 {v} 格式有误！应为 YYYYMMDD')
