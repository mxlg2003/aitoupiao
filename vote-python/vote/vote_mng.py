from fastapi import APIRouter, Request, Depends
from public.oppose_crawler import backstage
from core import config
from vote.form import ActivityListForm


__author__ = '吾延'
router = APIRouter()


@router.get('/list',  dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name='活动列表')
async def activity_list(request: Request, form: ActivityListForm):
    """
    活动列表
    """
