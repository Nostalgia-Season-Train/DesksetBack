from datetime import datetime


# 返回后端日期时间
def current():
    now = datetime.now()

    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "week": now.weekday(),
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second
    }
