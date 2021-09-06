from celery.schedules import crontab

# celery 配置文件
__author__ = '吾延'


# Broker ，即为任务调度队列，接收任务生产者发来的消息（即任务），将任务存入队列
broker_url = "redis://127.0.0.1:6379/9"   # 使用redis存储任务队列

# Backend 用于存储任务的执行结果，以供查询。
result_backend = "redis://127.0.0.1:6379/9"

# 指定任务序列化方式
task_serializer = 'json'
# 指定结果序列化方式
result_serializer = 'json'
# 指定任务接受的序列化类型.
accept_content = ['json']
# 时区设置
timezone = "Asia/Shanghai"
enable_utc = False
# celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
worker_hijack_root_logger = False
# 存储结果过期时间（默认1天）
result_expires = 60 * 60 * 24


# 导入任务所在的py文件
imports = [
    "celery_model.celery_task",
    "fund_shares.spider_fund",
    "fund_shares.spider_shares",
]

# 每分钟(minute="*/1") 周一至周五(day_of_week=[1, 2, 3, 4, 5]), 周六到周日(day_of_week=[0, 6])
# 需要执行任务的配置
beat_schedule = {
    "task1": {
        "task": "celery_model.celery_task.spider_fun_task",  # 要执行的方法
        "schedule": crontab(minute=36, hour=18, day_of_week=[1, 2, 3, 4, 5, 6]),   # 周一至周五每晚19:10开始执行爬虫程序
        "args": ()  # 方法参数
    },
    "task2": {
        "task": "fund_shares.spider_fund.spider_run",  # 要执行的方法
        "schedule": crontab(minute=30, hour=19, day_of_week=[1, 2, 3, 4, 5, 6]),   # 周一至周六每晚 19:40 开始执行爬虫程序
        "args": ()  # 方法参数
    },
    "task3": {
        "task": "fund_shares.spider_shares.get_shares_info",  # 要执行的方法
        "schedule": crontab(minute=50, hour=20, day_of_week=[1, 2, 3, 4, 5, 6]),   # 周一至周六每晚 21:20 开始执行爬虫程序
        "args": ()  # 方法参数
    },
}

