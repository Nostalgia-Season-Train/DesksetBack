import shutil, os

# ==== 预处理 ====

# 清除上次文件
shutil.rmtree('./dist/DigitalDeskSetup/site-packages')
shutil.rmtree('./dist/DigitalDeskSetup/i18n')


# ==== 打包 ====

# 下载依赖
os.system('pip install -r requirements.txt -t ./dist/DigitalDeskSetup/site-packages')

# 构建程序
os.system('nuitka --module src/deskset --include-package=deskset --output-dir=dist/DigitalDeskSetup/site-packages --remove-output')

# 复制 i18n 翻译文件
shutil.copytree('./i18n', './dist/DigitalDeskSetup/i18n')
