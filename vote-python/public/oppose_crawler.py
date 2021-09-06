import time
import base64
from fastapi import Request, HTTPException
from core import config
from public.str_utils import encrypt_password
from db.db_caches import cache
from sqlalchemy.orm import Session
from db.db_base import DbHandleBase
from system.model import SysOperationLog
from public.get_data_by_cache import get_token_key, get_current_user
__author__ = '吾延'


async def backstage(request: Request):
    """后台防爬方法"""""
    raw_list = request.headers.raw
    token_check = None
    referer = False
    for raw in raw_list:
        if bytes.decode(raw[0]) == 'tokencheck':
            token_check = bytes.decode(raw[1])
        if bytes.decode(raw[0]) == 'referer':
            referer_str = bytes.decode(raw[1])
            referer = True if referer_str.split('/')[3] == 'vote_docs' else False
    #  访问的是文档接口
    if referer:
        user = {'login_name': 'admin', 'user_name': '吾延', 'id': 15950378016551623}
        token_key = 'token' + encrypt_password(str(user['id']))
        if not cache.exists(token_key):
            token = 'token' + encrypt_password(str(user['id']))
            cache.set(token, str(user), config.REDIS_TIME_OUT)
    else:
        if request.url.path.split('/')[-1] != 'login' and request.url.path.split('/')[-1] != 'login-out' and request.url.path.split('/')[-1] !='get-setting':
            token = None
            for raw in raw_list:
                if bytes.decode(raw[0]) == 'token':
                    token = bytes.decode(raw[1])
            if token is None or not cache.get(token):
                raise HTTPException(status_code=403, detail='token失效，请重新登录')
        # 反爬逻辑
        # 1-2位是数字
        token_check_list = token_check.split('-')
        token_check_num = base64.b64decode(token_check_list[0])
        token_check_str = bytes.decode(base64.b64decode(token_check_list[1]))
        token_time = base64.b64decode(token_check_list[2])
        if int(token_check_num) < 9 or int(token_check_num) > 99:
            raise HTTPException(status_code=404, detail='数字-系统操作错误')
        # 3-4位 == JK
        if token_check_str != 'JK':
            raise HTTPException(status_code=404, detail='字母-系统操作错误')
        req_time = int(int(token_time) / 1000)  # 请求时间(秒)
        now_time = int(time.time())  # 当前时间(秒)
        # 如果请求时间与当前时间对比(前后复权100s)
        if (now_time + 100) < req_time or (now_time - 100) > req_time:
            # 当前时间加10s小于请求时间， 当前时间减20秒大于请求时间
            raise HTTPException(status_code=404, detail="超时-请求超时系统操作错误")
    # 插入操作日志
    operation_log(request)


async def onstage(request: Request):
    """
    前端反爬
    """


def operation_log(request):
    """
    插入日志
    """
    if not config.OPEN_OPERATION_LOG:
        return
    operation_type = "query"
    name = ""
    for route in request.app.routes:
        if request.scope['path'] == route.path:
            operation_type = route.tags[0] if route.tags else operation_type
            name = route.name
    # 是否开启查询日志
    if not config.OPEN_QUERY_OPERATION_LOG and operation_type == 'query':
        return

    token_key = get_token_key(request)
    if token_key:
        user = get_current_user(request)
        db: Session = request.state.db
        operation_log = SysOperationLog()
        dh_handle = DbHandleBase()
        browser = None
        operation_log.operation_url = request.scope['path']
        operation_log.ip = request.scope['client'][0]
        operation_log.login_name = user['login_name']
        operation_log.name = name
        for raw in request.headers.raw:
            if bytes.decode(raw[0]) == 'user-agent':
                browser = bytes.decode(raw[1])
        operation_log.browser = browser
        dh_handle.create(db, token_key, operation_log)
