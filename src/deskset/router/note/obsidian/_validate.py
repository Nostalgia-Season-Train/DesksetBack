from __future__ import annotations

from pydantic import BaseModel, field_validator

from deskset.core.standard import DesksetError


# ==== NoteAPI data.json 设置 ====
class Setting(BaseModel):
    host: str
    port: int
    username: str
    password: str

    profile: Profile
    greets: list[Greet]  # 允许空数组

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
    def current(cls) -> str:
        return arrow.now().format('HHmm')

    @field_validator('start', 'end')
    @classmethod
    def check_start(cls, v: str) -> str:
        try:
            arrow.get(v, 'HHmm')
            return v
        except arrow.ParserError:
            raise DesksetError(message=f'时间 {v} 格式错误，应为 HHmm')
        except ValueError:
            raise DesksetError(message=f'时间 {v} 无效')
