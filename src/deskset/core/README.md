数字桌搭：核心代码 core

# config
配置


# locale
本地化

使用：
- 1、_t('translate')
- 2、i18n：translate: 翻译
- 3、效果：_t('translate') = '翻译'


# standard
错误及日志


# text file
文本文件

使用：
- 打开/关闭：不依靠调用方管理 None 状态
- 读取/写入：
    - 每次读取，都会同步内存与硬盘中数据
    - 每次写入，都会检查内存与硬盘中数据，如果不一致则抛出异常
- 撤销/重做


# root path
根路径

使用：将一个文件夹视作根路径，操作文件夹中的文件
