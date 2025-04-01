from apscheduler.schedulers.asyncio import AsyncIOScheduler

from deskset.router.note.noteapi import noteapi

async def hello():
    # Python 通过 create_task 协程，实现异步请求立即返回
    import asyncio
    asyncio.create_task(noteapi.get('/obsidian/hello'))

apscheduler = AsyncIOScheduler(job_defaults={ 'misfire_grace_time': 30 })  # 错过约定时间后，30s 之内仍会执行
apscheduler.add_job(hello, 'interval', seconds=5)


# 禁止 apscheduler 输出 ERROR 级别以下的日志
import logging

logging.getLogger('apscheduler').setLevel(logging.ERROR)
