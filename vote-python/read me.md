# love_vote

#### 介绍
爱投票管理系统


##### 1、配置好环境之后，使用 alembic init 命令生成 alembic 目录和alembic.ini文件
##### 2、将alembic.ini 文件中的 sqlalchemy.url 注释掉
##### 3、修改 alembic 目录下的env.py 文件
##### 4、使用命令 alembic revision --autogenerate 创建迁移文件
##### 5、使用命令 alembic upgrade head 迁移数据库
##### 6、数据库操作
##### 7、运行：1、直接运行main.py 文件  2、使用命令运行：uvicorn main:app --reload --port 8088


# 使用清华源安装依赖 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt


# 创建单条记录
# from db.db_base import DbHandleBase
# user = SysUser()
# user.login_name = 'login_name'
# user.password = encrypt_password('password')
# user.user_name = 'login_name'
# user.phone = '13737170000'
# token_key = get_token_key(request)
# handle_db = DbHandleBase()
# status_code, dept_obj = handle_db.create(db, token_key, dept)

# 查看执行的SQL print(str(SysUser.query(SysUser.id, SysUser.user_name).filter(SysUser.state==1).all()))