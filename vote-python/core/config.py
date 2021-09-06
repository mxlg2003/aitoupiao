__author__ = '吾延'

# 数据库连接, 多个数据库可用元组
# '数据库类型+数据库驱动名称://用户名:数据库密码@数据库连接地址:端口号/数据库名'
DB_CONN_URI = "mysql+pymysql://root:root@localhost:3306/love_vote"

# redis连接
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_TIME_OUT = 5 * 60 * 60    # 缓存时间默认三小时

# 是否记录操作日志
OPEN_OPERATION_LOG = True
# 是否记录查询操作日志
OPEN_QUERY_OPERATION_LOG = False
# 操作日志查询
LOG_QUERY = "query"
# 操作日志保存
LOG_SAVE = "save"
# 操作日志删除
LOG_DELETE = "delete"


# 当前登录系统的用户
CURR_SYS_USER = 'CURR_SYS_USER'

# 跨域白名单
ALLOW_ORIGINS = ['*']

# 默认文件存放根目录文件
STATIC_DIR = 'media'

# 返回结果代码
HTTP_200 = 200      # 请求正常
HTTP_400 = 400      # 登录报错
HTTP_403 = 403      # token失效，强制退出登录
HTTP_404 = 404      # 系统报错
