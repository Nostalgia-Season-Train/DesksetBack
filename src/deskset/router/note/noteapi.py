from httpx import AsyncClient

from deskset.core.config import config

noteapi = AsyncClient(base_url=f'http://{config.noteapi_host}:{config.noteapi_port}')
