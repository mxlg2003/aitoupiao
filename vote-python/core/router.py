from fastapi import APIRouter
from system import urls as auth_urls
from vote import urls as vote_urls
from wechat import urls as wechat_urls
from wechat_api import urls as api_urls
from fund_shares import urls as fund_urls
from public.upload_file_utils import router as upload_router

__author__ = '吾延'
api_router = APIRouter()

# 全局路由
api_router.include_router(auth_urls.auth_router, prefix='/system')
api_router.include_router(vote_urls.vote_router, prefix='/vote')
api_router.include_router(wechat_urls.wechat_router, prefix='/wechat')
api_router.include_router(api_urls.api_router, prefix='/wechat-api')
api_router.include_router(fund_urls.fund_router, prefix='/fund-shares')
api_router.include_router(upload_router, prefix='/file')
