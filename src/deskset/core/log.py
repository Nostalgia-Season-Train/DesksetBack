import logging

logging.basicConfig(
    filename='log/latest.log',
    filemode='w',  # 注：目录不存在也会抛出 FileNotFoundError 异常
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)
