from fastapi import APIRouter
from system import auth_mng, department_mng, role_mng, menu_mng, user_mng, log_mng

__author__ = '吾延'
auth_router = APIRouter()

# 系统、权限路由
auth_router.include_router(auth_mng.router, prefix='/auth')
auth_router.include_router(department_mng.router, prefix='/dept')
auth_router.include_router(role_mng.router, prefix='/role')
auth_router.include_router(menu_mng.router, prefix='/menu')
auth_router.include_router(user_mng.router, prefix='/user')
auth_router.include_router(log_mng.router, prefix='/log')
