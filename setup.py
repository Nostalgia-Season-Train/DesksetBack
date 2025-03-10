import shutil, os

RUNON = 'res/PyStand/PyStand-v1.1.4+Python-v3.9.7.zip'
DIST = 'dist/DesksetBack'  # 构建产物的存放路径

def clear(folder):
    shutil.rmtree(f'./{DIST}/{folder}', ignore_errors=True)
def copy(folder):
    shutil.copytree(f'./{folder}', f'./{DIST}/{folder}')


# ==== 预处理 ====

# 清除上次构建
shutil.rmtree(f'./{DIST}', ignore_errors=True)

# 创建运行环境
import zipfile

os.makedirs(f'./{DIST}', exist_ok=True)

with zipfile.ZipFile(f'./{RUNON}', 'r') as file:
    file.extractall(f'./{DIST}')


# ==== 打包 ====

# 下载依赖
os.system(f'pip install -r requirements.txt -t ./{DIST}/site-packages')

# 构建程序
  # 构建失败的解决方案
  # - Error 1104：避免中文路径
os.system(f'nuitka --module src/deskset --include-package=deskset --output-dir={DIST}/site-packages --remove-output')

# 编译 C/C++ 代码
os.makedirs(f'./lib', exist_ok=True)  # 创建 lib 二进制库，否则 gcc 报错

os.system('cd src/package_C/disk_active_time && build.bat')

copy('lib')

# 复制 翻译文件、示例插件
copy('i18n')
copy('api')


# ==== 压缩 ====
shutil.make_archive('./dist/DesksetBack', 'zip', f'./{DIST}')  # 压缩包主名，压缩格式，压缩路径
