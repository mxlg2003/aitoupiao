from sqlalchemy import String, Column, SmallInteger, Boolean, Integer, DateTime
from db.db_base import BaseModel

__author__ = '吾延'


class WechatSubscriber(BaseModel):
    _table_name_ = 'wechat_subscriber'
    __table_args__ = ({'comment': '微信订阅者表'})
    openid = Column(String(length=50), nullable=False, comment='微信openId')
    union_id = Column(String(length=100), nullable=True, comment='订阅者唯一的id')
    wachet_no = Column(String(length=100), nullable=True, comment='微信号')
    nickname = Column(String(length=100), nullable=True, comment='微信名')
    sex = Column(SmallInteger, default=0, comment='性别, 0为未知,1为男,2为女')
    province = Column(String(length=100), nullable=True, comment='省份')
    city = Column(String(length=100), nullable=True, comment='城市')
    country = Column(String(length=100), nullable=True, comment='国家')
    head_img_url = Column(String(length=1300), nullable=True, comment='头像')
    privilege = Column(String(length=100), nullable=True, comment='特权')
    subscribed = Column(Boolean, default=False, comment='目前已取消关注')
    subscribe_time = Column(DateTime, nullable=True, comment='关注时间')
    unsubscribe_time = Column(DateTime, nullable=True, comment='取消关注时间')
    latitude = Column(String(length=20), nullable=True, comment='纬度')
    longitude = Column(String(length=20), nullable=True, comment='经度')
    precision = Column(String(length=20), nullable=True, comment='精度')
    tags = Column(String(length=100), nullable=True, comment='标签')
    points = Column(Integer, default=0, comment='微信卡券积分')
