import logging

logging.basicConfig(
    filename='log/latest.log',
    filemode='w+',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)
