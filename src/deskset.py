# 入口文件
# 作用：当成 Digital Desk Setup 程序根目录
# - 确保绝对导入 import deskset 正常工作
# - 确保资源文件 resource, i18n 正确解析
# - 模拟实际安装目录

from deskset.main import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)

# 推荐环境配置：
# 在项目目录下添加 .env 文件，输入以下内容
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__
