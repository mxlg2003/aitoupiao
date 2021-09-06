from sqlalchemy import String, Column, DateTime, Boolean, Text, Integer, SmallInteger
from db.db_base import BaseModel

__author__ = '吾延'


class VoteActivity(BaseModel):
    # 表名
    _table_name_ = 'vote_activity'
    __table_args__ = ({'comment': '投票活动表'})
    activity_title = Column(String(50), index=True, nullable=False, comment='活动标题')
    background_img = Column(String(length=300), nullable=False, comment='活动底图图片链接')
    posters_img = Column(String(300), nullable=False, comment='活动海报图片链接')
    start_time = Column(DateTime, nullable=False, comment='活动开始时间')
    end_time = Column(DateTime, nullable=False, comment='活动结束时间')
    activity_info = Column(String(3000), nullable=True, comment='活动详情')
    organizers_info = Column(String(3000), nullable=True, comment='主办方信息')
    # 权限限制
    user_vote_total = Column(Integer, nullable=False, default=0, comment='用户投票总次数')
    user_day_vote_num = Column(Integer, nullable=False, default=1, comment='用户每天投票次数')
    allow_repeat_vote = Column(Boolean, nullable=False, default=True, comment='允许单日同一项重复被投票')
    # 展示设置
    show_ticket_Num = Column(Boolean, nullable=False, default=True, comment='是否显示票数， 默认显示')
    show_supporters_list = Column(Boolean, nullable=False, default=True, comment='是否在选手详情页显示支持者，默认显示')
    # 分享设置
    default_share = Column(Boolean, nullable=False, default=True, comment='是否默认分享设置，默认是')
    share_title = Column(String(50), nullable=True, comment='分享标题')
    share_desc = Column(String(100), nullable=True, comment='分享描述')
    share_img = Column(String(300), nullable=True, comment='分享图片链接')
    # 开启评论
    open_comment = Column(Boolean, nullable=False, default=False, comment='是否支持投票后评论，默认不支持')
    # 活动票数
    total_ticket_num = Column(Integer, nullable=False, default=0, comment='总票数')
    # 总访问数
    total_visit_num = Column(Integer, nullable=False, default=0, comment='总访问数')
    # 审核
    approval_result = Column(SmallInteger, nullable=False, default=0, comment='审核结果::0未审核，1审核通过，2审核不通过')
    approval_user_id = Column(String(length=20), nullable=True, comment='审核用户id')
    approval_time = Column(DateTime, nullable=True, comment='时间')


class VoteItem(BaseModel):
    _table_name_ = 'vote_item'
    __table_args__ = ({'comment': '投票选手表'})
    item_name = Column(String(50), index=True, nullable=False, comment='选手名称')
    item_img = Column(String(300), nullable=False, comment='选手图片')
    item_no = Column(Integer, nullable=False, default=1, comment='选手编号')
    ticket_num = Column(Integer, nullable=False, default=0, comment='票数')
    item_info = Column(Text, nullable=True, comment='选手详情')


class VoteUser(BaseModel):
    _table_name_ = 'vote_user'
    __table_args__ = ({'comment': '投票用户表'})
    item_id = Column(String(length=20), index=True, nullable=False, comment='选手id')


class VoteComment(BaseModel):
    _table_name_ = 'vote_comment'
    __table_args__ = ({'comment': '投票评论表'})
    item_id = Column(String(length=20), index=True, nullable=False, comment='选手id')
    comment = Column(String(length=200), nullable=False, comment='评论内容')
    like_num = Column(Integer, nullable=False, default=0, comment='点赞数')


class VoteCommentLike(BaseModel):
    _table_name_ = 'vote_comment_like'
    __table_args__ = ({'comment': '评论点赞表'})
    comment_id = Column(String(length=20), index=True, nullable=False, comment='评论id')
