# === 检查参数 ===
import sys
args = sys.argv
DEVELOP_ENV = True if '-dev' in args else False


# === 运行程序 ===
from multiprocessing import freeze_support

print()  # 从 > 下一行开始打印

if __name__ == '__main__':
    freeze_support()  # 唯一的作用，就是排除由于 freeze_support 没有添加引发的错误
    if DEVELOP_ENV:
        import uvicorn
        uvicorn.run('deskset.main:app', host='127.0.0.1', port=6527, reload=True)
    else:
        # -dev 启动，虽然经过判断，但是下面的代码仍会执行，导致默认端口 6527 重复占用
          # 暂时不处理
        from deskset import main
        main()
