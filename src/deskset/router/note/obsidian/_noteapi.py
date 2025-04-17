from httpx import AsyncClient

from deskset.core.config import config

noteapi = AsyncClient(base_url=f'http://{config.noteapi_host}:{config.noteapi_port}')


# 禁止 httpx 输出 ERROR 级别以下的日志
import logging

logging.getLogger('httpx').setLevel(logging.ERROR)
