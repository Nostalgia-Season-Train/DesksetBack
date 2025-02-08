# 开发时，从这里运行服务器
# - 1、避免循环引用
# - 2、模拟生产环境

from deskset import main
main()

# 注：如果报错，创建 .env 文件
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__  # 可选，统一缓存位置
