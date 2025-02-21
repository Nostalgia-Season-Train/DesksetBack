# 命令行参数
from argparse import ArgumentParser

parser = ArgumentParser(description='数字桌搭后端命令行参数')
parser.add_argument('-dev', action='store_true', help='以开发者环境启动')
args = parser.parse_args()

DEVELOP_ENV = args.dev
DEBUG_MODE  = False  # 调试模式


# 日志
from deskset.core.log import logging

if DEVELOP_ENV:
    logging.info('Running on Development Environment')
if DEBUG_MODE:
    logging.info('Open Debug Mode')


# 设置服务器端口
from deskset.core.config import config

server_port = config.server_port
logging.info(f'Server Port {server_port}')


# FastAPI 程序
# ！！！警告，需要身份验证，不然任意桌面应用程序都能访问本服务器！！！
# 一个 CSRF 示例：<img src="http://127.0.0.1:8000/v0/device/cpu"></img>，可在其他 Electron 程序中访问本服务器接口
from fastapi import FastAPI

app = FastAPI()


# CORS 跨域请求
if DEVELOP_ENV:  # 开发时有 Vite Server 需要添加 CORS
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins='http://127.0.0.1:5173',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    logging.info(f'Add http://127.0.0.1:5173 to CORS')


# 统一错误（异常）处理
from fastapi.requests import Request
from deskset.core.standard import DesksetError
from fastapi.responses import JSONResponse
from deskset.presenter.format import format_return
from http import HTTPStatus

@app.exception_handler(DesksetError)
def deskset_error(request: Request, err: DesksetError):
    # JSONResponse 编码默认 utf-8，deskset config 暂时无法影响
    return JSONResponse(
        # status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=format_return(err)
    )

@app.exception_handler(Exception)
def deskset_exception(request: Request, exc: Exception):
    logging.exception(exc, exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=str(exc)
    )


# 认证接口
from deskset.router.access import router_access
app.include_router(router_access)


# 调试接口
if DEBUG_MODE:
    from deskset.router.debug import router_debug
    app.include_router(router_debug)


# 路由注册
from deskset.router.device import router_device
app.include_router(router_device)

from deskset.router.obsidian import router_obsidian
app.include_router(router_obsidian)

from deskset.router.greet import router_greet
app.include_router(router_greet)

from deskset.router.current import router_datetime
app.include_router(router_datetime)

# from deskset.router.cloud import router_cloud
# app.include_router(router_cloud)

from deskset.router.quick import router_quick
app.include_router(router_quick)

from deskset.router.config import router_config
app.include_router(router_config)


# 插件注册：/api 作为所有插件路由的根路径
from deskset.router.plugin import router_plugin_root
app.include_router(router_plugin_root)


# 启动服务器
def main():
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=server_port)
