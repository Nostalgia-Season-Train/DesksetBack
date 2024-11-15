import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from asyncer import asyncify

from deskset.core.standard import DesksetError


# 实例化 FastAPI 并注册路由
app = FastAPI()

from deskset.router.device import router_device
from deskset.router.diary import router_diary

app.include_router(router_device)
app.include_router(router_diary)


# 启动服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
