import shutil, os

DIST = 'dist/Deskset-Back'  # 构建产物的存放路径

def clear(folder):
    shutil.rmtree(f'./{DIST}/{folder}', ignore_errors=True)
def copy(folder):
    shutil.copytree(f'./{folder}', f'./{DIST}/{folder}')


# ==== 预处理 ====

# 清除上次构建和测试产生的文件及文件夹
clear('site-packages')
clear('lib')

clear('config')
clear('log')

clear('i18n')

clear('api')


# ==== 打包 ====

# 下载依赖
os.system(f'pip install -r requirements.txt -t ./{DIST}/site-packages')

# 构建程序
  # 构建失败的解决方案
  # - Error 1104：避免中文路径
os.system(f'nuitka --module src/deskset --include-package=deskset --output-dir={DIST}/site-packages --remove-output')

# 编译 C/C++ 代码
os.system('cd src/package_C/disk_active_time && build.bat')

copy('lib')

# 复制 翻译文件、示例插件
copy('i18n')
copy('api')


# ==== 压缩 ====
shutil.make_archive('./dist/Deskset-Back', 'zip', f'./{DIST}')  # 压缩包主名，压缩格式，压缩路径
