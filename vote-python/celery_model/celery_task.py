from celery import Celery
import datetime
from fund_shares.spider_fund import spider_run
from fund_shares.spider_shares import get_shares_info
from public.logger import logger


__author__ = '吾延'
celery_app = Celery()


@celery_app.task()
def spider_fun_task():
    logger.info('==============================进入定时任务===============================')
