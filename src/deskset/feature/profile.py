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

def load_profile():
    global profile  # 闭包
    try:
        with open(CONF_PROFILE_PATH, 'r', encoding=CONF_PROFILE_ENCODE) as file:
            data: dict = yaml_load(file)
            for attr_key, _ in list(profile.__dict__.items()):
                setattr(profile, attr_key, data.get(attr_key))
            # 错误方法：这会让本文件内的 profile 指针指向新实例
            # profile = Profile.model_validate(yaml_load(file))
    except Exception as exc:
        logging.exception(exc, exc_info=exc)

def save_profile():
    global profile
    try:
        with open(CONF_PROFILE_PATH, 'w', encoding=CONF_PROFILE_ENCODE) as file:
            yaml_dump(profile.model_dump(), file, allow_unicode=True, sort_keys=False)
    except Exception as exc:
        logging.exception(exc, exc_info=exc)

load_profile()
save_profile()
