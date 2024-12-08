from fastapi import FastAPI

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
async def deskset_error(request: Request, error: DesksetError):
    # JSONResponse 编码默认 utf-8，deskset config 暂时无法影响
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=format_return(error)
    )


# 路由注册
from deskset.router.device import router_device
app.include_router(router_device)

from deskset.router.diary import router_diary
app.include_router(router_diary)

from deskset.router.greet import router_greet
app.include_router(router_greet)

from deskset.router.datetime import router_datetime
app.include_router(router_datetime)


# 一个标准接口，测试前端请求
from deskset.core.locale import _t
from deskset.presenter.format import format_return

@app.get('/helloworld')
async def hello_world():
    def execute_function():
        return _t('helloworld')

    return format_return(execute_function())


# 启动服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=SEVER_LOCAL_PORT)
