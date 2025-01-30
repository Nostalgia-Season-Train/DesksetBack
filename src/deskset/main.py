from fastapi import FastAPI

DEBUG_MODE = True  # 调试模式

FRONT_LOCAL_PORT = 5173  # 前端端口号
SEVER_LOCAL_PORT = 8000  # 后端端口号


# FastAPI 程序
app = FastAPI()


# CORS 跨域请求
from fastapi.middleware.cors import CORSMiddleware

origins = ['http://localhost:' + str(FRONT_LOCAL_PORT)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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

import logging

@app.exception_handler(Exception)
def deskset_exception(request: Request, exc: Exception):
    logging.exception(exc, exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=str(exc)
    )


# 调试接口
if DEBUG_MODE:
    from deskset.router.debug import router_debug
    app.include_router(router_debug)


# 路由注册
from deskset.router.device import router_device
app.include_router(router_device)

from deskset.router.diary import router_diary
app.include_router(router_diary)

from deskset.router.greet import router_greet
app.include_router(router_greet)

from deskset.router.current import router_datetime
app.include_router(router_datetime)

from deskset.router.cloud import router_cloud
app.include_router(router_cloud)


# 插件注册：/api 作为所有插件路由的根路径
from deskset.router.plugin import router_plugin_root
app.include_router(router_plugin_root)


# 一个标准接口，测试前端请求
from deskset.core.locale import _t
from deskset.presenter.format import format_return

@app.get('/helloworld')
async def hello_world():
    def execute_function():
        return _t('helloworld')

    return format_return(execute_function())


# 启动服务器
def main():
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=SEVER_LOCAL_PORT)


# 开发服务器
if __name__ == '__main__':
    main()
