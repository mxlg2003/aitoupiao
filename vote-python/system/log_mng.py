from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from public.oppose_crawler import backstage
from system.model import SysLoginLog as Login, SysOperationLog as Ope
from public.data_utils import orm_all_to_dict
from core import config


__author__ = '吾延'
router = APIRouter()


@router.get('/login-log', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="登录日志列表")
async def login_log(request: Request, login_name: str = None, time_start: str = None, time_end: str = None):
    """
    登录日志列表
    """
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('pageSize', 10))
    start = (page - 1) * page_size
    db: Session = request.state.db
    db_log = db.query(Login.id, Login.login_name, Login.user_name, Login.is_success,
                      Login.create_time,
                      Login.browser, Login.login_ip).filter(Login.state == 1)
    if login_name:
        db_log = db_log.filter(Login.login_name.like('%' + login_name + '%'))
    if time_start:
        db_log = db_log.filter(Login.create_time >= time_start)
    if time_end:
        db_log = db_log.filter(Login.create_time <= time_end)
    total = db_log.count()
    orm_logs = db_log.order_by(Login.create_time.desc()).limit(page_size).offset(start).all()

    login_log_list = orm_all_to_dict(orm_logs)
    return JSONResponse({'code': config.HTTP_200, 'data': {'log_list': login_log_list, 'total': total}})


@router.get('/operate-log', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="操作日志列表")
async def operate_log(request: Request, login_name: str = None, ope_name: str = None, time_start: str = None,
                      time_end: str = None):
    """
    操作日志列表
    """
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('pageSize', 10))
    start = (page - 1) * page_size
    db: Session = request.state.db
    db_log = db.query(Ope.id, Ope.name, Ope.operation_url, Ope.ip,
                      Ope.browser,  Ope.create_time,
                      Ope.login_name).filter(Ope.state == 1)
    if login_name:
        db_log = db_log.filter(Ope.login_name.like('%' + login_name + '%'))
    if ope_name:
        db_log = db_log.filter(Ope.name.like('%' + ope_name + '%'))
    if time_start:
        db_log = db_log.filter(Ope.create_time >= time_start)
    if time_end:
        db_log = db_log.filter(Ope.create_time <= time_end)
    total = db_log.count()
    orm_logs = db_log.order_by(Ope.create_time.desc()).limit(page_size).offset(start).all()
    operate_log_list = orm_all_to_dict(orm_logs)
    return JSONResponse({'code': config.HTTP_200, 'data': {'operateList': operate_log_list, 'total': total}})
