import requests
import json
import re
from db.session import SessionLocal
from sqlalchemy.orm import Session
from fund_shares.model import FundInfo, FundEquity
from public.logger import logger
from celery import Celery


__author__ = '吾延'
celery_app = Celery()


def get_fund_list():
    """
    第一级爬虫 - 爬取列表信息
    """
    shares_fund_url = ""
    res = requests.request(method='get', url=shares_fund_url)
    fund_list = json.loads(res).get('datas')

    return fund_list


def get_fund_info(db: Session, fund_data):
    """
    第二级爬虫 - 爬取详细信息
    """
    fund_info = dict()
    fund_equity_info = dict()
    try:
        # 数据入库
        insert_data(db, fund_info, fund_equity_info)
    except Exception as e:
        logger.error(e)


def handle_float_num(num_str):
    """
    处理返回的获取到的数字数据
    """
    has_num = re.findall(r"\d+\.?\d*", num_str)
    if not has_num:
        result = None
    elif num_str.find('-') != -1:
        result = float('-' + has_num[0])
    else:
        result = has_num[0]
    return result


def insert_data(db: Session, fund_info, equity_info):
    """
    数据入库
    """
    fund_no = fund_info.get('fund_no')
    unit_date = equity_info.get('unit_date')
    try:
        if fund_no and not db.query(FundInfo.fund_no).filter(FundInfo.fund_no == fund_no).scalar():
            new_fund_info = FundInfo()
            new_fund_info.fund_no = fund_no
            new_fund_info.fund_name = fund_info.get('fund_name')
            db.add(new_fund_info)
            db.commit()
    except Exception as e:
        logger.error(e)
        db.rollback()
    try:
        if unit_date and not db.query(FundEquity.unit_date).filter(FundEquity.fund_no == fund_no, FundEquity.unit_date == unit_date).scalar():
            fund_equity = FundEquity()
            fund_equity.unit_date = unit_date
            fund_equity.fund_no = fund_no
            db.add(fund_equity)
            db.commit()
    except Exception as e:
        logger.error(e)
        db.rollback()


@celery_app.task()
def spider_run():
    """
    执行爬虫程序
    """
    db: Session = SessionLocal()
    logger.info('=========================进入爬虫方法=========================')
    fund_data_list = get_fund_list()
    for fund_data in fund_data_list:
        get_fund_info(db, fund_data)


if __name__ == '__main__':
    spider_run()








