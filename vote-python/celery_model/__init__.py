from celery import Celery

__author__ = '吾延'

# Windows开发调试直接启动即可
# 启动： celery -A celery_model beat
# 执行： celery -A celery_model worker

# 创建celery应用对象
celery_app = Celery("celery_demo")

# 导入celery的配置信息
celery_app.config_from_object("celery_model.celery_config")
celery_app.conf.timezone = 'Asia/Shanghai'

# 配置参考： https://www.cnblogs.com/yinzhuoqun/p/10939936.html

# 安装 supervisor
# yum install supervisor
# # 设置开机启动
# systemctl enable supervisord.service
# # 上面这个步骤会生成 supervisor 配置文件：/etc/supervisord.conf 和 supervisor配置文件目录 /etc/supervisord.d
# # 启动 supervisor 后会 启动 /etc/supervisord.d 文件夹下以 .ini 为后缀的文件中的进程命令
# # supervisor 相关命令
# 启动： systemctl start supervisord.service
# 停止： systemctl stop supervisord.service
# 重启： systemctl restart supervisord.service
#
# 新增配置文件后需要更新配置, .ini文件必须是utf-8编码，不然重启会报错
# supervisorctl update
#
# # supervisord 管理进程的相关命令
# supervisorctl stop CeleryBeat                #关闭 CeleryBeat
# supervisorctl start CeleryBeat               #启动 CeleryBeat
# supervisorctl restart CeleryBeat             #重启 CeleryBeat
# supervisorctl update                          #更新新的配置

# 执行异步任务前需要重启项目
# #celery_beat.ini 配置文件 启动命令：supervisorctl start CeleryBeat
# [program:CeleryBeat]
# directory=/data/wwwroot/love_vote	; 命令执行的目录
# command=/data/env/love_vote/bin/celery -A celery_model beat --loglevel=info	; 执行的命令（需要加上celery的位置，不然找不到）
# autostart=true		; 是否自启动
# autorestart=true	; 是否自动重启
# startsecs=3			; 自动重启时间间隔（s）
# stderr_logfile=/data/celery_log/celerybeat.err.log		; 错误日志文件
# stdout_logfile=/data/celery_log/celerybeat.out.log		; 输出日志文件
#
# celery_work.ini 配置文件 启动命令：supervisorctl start CeleryWork
# [program:CeleryWork]
# directory=/data/wwwroot/love_vote	; 命令执行的目录
# command=/data/env/love_vote/bin/celery -A celery_model worker --loglevel=info	; 执行的命令（需要加上celery的位置，不然找不到）
# autostart=true		; 是否自启动
# autorestart=true	; 是否自动重启
# startsecs=3			; 自动重启时间间隔（s）
# stderr_logfile=/data/celery_log/celerywork.err.log		; 错误日志文件
# stdout_logfile=/data/celery_log/celerywork.out.log		; 输出日志文件
