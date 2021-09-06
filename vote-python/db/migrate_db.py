from db.db_base import BaseDB
from system import model
from vote import model
from wechat import model
from fund_shares import model


# 需要将各模块的model引到此文件才能被alembic的env.py引用，才能将各模块的表迁移成功
__author__ = '吾延'
