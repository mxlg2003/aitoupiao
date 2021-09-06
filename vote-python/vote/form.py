from pydantic import BaseModel
from _datetime import datetime

__author__ = '吾延'


class ActivityListForm(BaseModel):
    pass


class ActivitySaveForm(BaseModel):
    """活动新增、修改form"""
    id: str = None
    activity_title: str
    template: str
    posters_img: str
    start_time: datetime
    end_time: datetime
    activity_info: str = None
    organizers_info: str = None
    # 权限限制
    user_vote_total: int = 0
    user_day_vote_num: int = 1
    allow_repeat_vote: bool = True
    # 展示设置
    show_type: bool = True
    show_ticket_Num: bool = True
    show_ranking_list: bool = True
    show_supporters_list: bool = True
    # 分享设置
    default_share: bool = True
    share_title: str = None
    share_desc: str = None
    share_img: str = None
    # 开启评论
    open_comment: bool = False
    # 活动票数
    total_ticket_num: int = 0
    # 总访问数
    total_visit_num: int = 0
    # 审核
    approval_result: int = 0
    approval_user_id: str = None
    approval_time: datetime = None
