from __future__ import annotations

from pydantic import BaseModel, field_validator
from asyncer import asyncify

from deskset.core.standard import DesksetError


# ==== NoteAPI data.json 设置 ====
class Setting(BaseModel):
    host: str
    port: int
    username: str
    password: str

    profile: Profile
    greets: list[GreetID]  # 允许空数组

# ID 标识符
  # 与其他模型组合以附加 id 属性
class ID(BaseModel):
    id: str  # 标识符 = YYYYMMDDHHmmss(创建日期时间) + 000000(同一时刻生成顺序)

    @field_validator('id')
    @classmethod
    def check_id(cls, v: str) -> str:
        if len(v) != 20:
            raise DesksetError(message=f'标识符 {v} 长度错误，不等于 20')
        return v

# 个性资料
class Profile(BaseModel):
    avatar: str
    name: str
    bio: str

# 问候语
import arrow

class Greet(BaseModel):
    start: str  # 开始时间 HHmm
    end: str    # 结束时间 HHmm
    open: str     # 开场白（例：早上好）
    content: str  # 问候内容（例：今天也是元气满满的一天！）

    # 当前时间 HHmm
    @classmethod
    async def current(cls) -> str:
        now = await asyncify(arrow.now)()
        current = await asyncify(now.format)('HHmm')
        return current

    @field_validator('start', 'end')
    @classmethod
    def check_time(cls, v: str) -> str:
        try:
            arrow.get(v, 'HHmm')
            return v
        except arrow.ParserError:
            raise DesksetError(message=f'时间 {v} 格式错误，应为 HHmm')
        except ValueError:
            raise DesksetError(message=f'时间 {v} 无效')

class GreetID(Greet, ID):
    pass
