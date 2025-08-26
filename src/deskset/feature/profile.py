from pydantic import BaseModel, field_validator

CONF_PROFILE_PATH = './config/profile.yaml'
CONF_PROFILE_ENCODE = 'utf-8'

class Profile(BaseModel, validate_assignment=True):
    name: str = '数字桌搭'
    bio: str = '数字桌搭，桌面美化与笔记应用的完美互动'

    @field_validator('name')
    @classmethod
    def check_name(cls, v: str) -> str:
        if v == '':
            raise ValueError(f'Name cannot be empty')
        return v

profile = Profile()


# ==== 先读再写 ====
from yaml import safe_load as yaml_load, dump as yaml_dump
from deskset.core.log import logging

try:
    with open(CONF_PROFILE_PATH, 'r', encoding=CONF_PROFILE_ENCODE) as file:
        profile = Profile.model_validate(yaml_load(file))
except Exception as exc:
    logging.exception(exc, exc_info=exc)

try:
    with open(CONF_PROFILE_PATH, 'w', encoding=CONF_PROFILE_ENCODE) as file:
        yaml_dump(profile.model_dump(), file, allow_unicode=True, sort_keys=False)
except Exception as exc:
    logging.exception(exc, exc_info=exc)
