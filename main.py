# 开发时，从这里运行服务器
# - 1、避免循环引用
# - 2、模拟生产环境


# === 检查参数 ===
import sys
args = sys.argv
DEVELOP_ENV = True if '-dev' in args else False


# === 运行程序 ===
if __name__ == '__main__':  # 保护程序入口点，避免热重载时，子进程重复执行
    if DEVELOP_ENV:
        # 1、如果在 src/deskset/main.py 使用，必须手动刷新 vscode git 才会显示仓库变化
        # 2、用 deskset.main:app 而不是 src.deskset.main:app（触发循环引用）
        import uvicorn
        uvicorn.run('deskset.main:app', host='127.0.0.1', port=6527, reload=True)
    else:
        from deskset import main
        main()


# 注：如果报错，创建 .env 文件
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__  # 可选，统一缓存位置
