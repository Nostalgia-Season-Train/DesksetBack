from pydantic import BaseModel

class Setting(BaseModel):
    host: str
    port: int
    username: str
    password: str
