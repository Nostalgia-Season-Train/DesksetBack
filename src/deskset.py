# 入口文件
# 唯一作用是作为顶层目录，让绝对导入 import deskset 能正常工作
# 很愚蠢，同时很有效

from deskset.main import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)

# PS：确实，有 N 种方法可以导入
# 但那些都太麻烦了

# 这里是推荐的环境设置：
# 在项目根目录下添加 .env
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__
