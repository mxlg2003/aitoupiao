import requests
import json
import datetime
import time
from db.session import SessionLocal
from sqlalchemy.orm import Session
from fund_shares.model import SharesInfo
from public.logger import logger
from celery import Celery


__author__ = '吾延'
celery_app = Celery()


db: Session = SessionLocal()


@celery_app.task()
def get_shares_info():
    """
    爬取方法
    """
    logger.info('=========================进入爬取方法=========================')
    time_s = str(int(time.time())) + '000'
    params = {'cb': f'jQuery1123006733026441095458_{time_s}'}
    res = requests.request(method='get', url='', params=params)
    res.encoding = 'utf-8'
    res_str = res.text
    json_list = json.loads(res_str).get('data')
    for shares in json_list:
        try:
            db_shares = SharesInfo()
            db_shares.shares_no = shares.get('f12')
            db_shares.shares_name = shares.get('f14')
            db.add(db_shares)
            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()


if __name__ == '__main__':
    get_shares_info()

