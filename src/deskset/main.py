from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deskset.presenter.format import format_return

FRONT_LOCAL_PORT = 5173  # 前端端口号
SEVER_LOCAL_PORT = 8000  # 后端端口号


# FastAPI 程序
app = FastAPI()


# CORS 跨域请求
origins = ["http://localhost:" + str(FRONT_LOCAL_PORT)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.get('/helloworld')
async def hello_world():
    return format_return(lambda : 'Hello World')


# 启动服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=SEVER_LOCAL_PORT)
