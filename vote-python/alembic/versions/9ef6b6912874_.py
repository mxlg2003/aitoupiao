"""empty message

Revision ID: 9ef6b6912874
Revises: a2aeb71e3351
Create Date: 2020-08-17 21:46:34.820905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef6b6912874'
down_revision = 'a2aeb71e3351'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote_activity_manage',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('change_by_id', sa.BigInteger(), nullable=True, comment='最后修改者ID'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('deleted_by_id', sa.BigInteger(), nullable=True, comment='删除者id'),
    sa.Column('activity_name', sa.String(length=100), nullable=False, comment='活动名称'),
    sa.Column('activity_img', sa.String(length=300), nullable=False, comment='活动图片'),
    sa.Column('showcase_img', sa.String(length=300), nullable=False, comment='橱窗图'),
    sa.Column('start_data', sa.Date(), nullable=False, comment='活动开始日期'),
    sa.Column('end_data', sa.Date(), nullable=False, comment='活动结束日期'),
    sa.Column('bg_color', sa.String(length=30), nullable=True, comment='背景颜色'),
    sa.Column('limit_vote', sa.Boolean(), nullable=True, comment='投票次数是否限制'),
    sa.Column('limit_type', sa.SmallInteger(), nullable=True, comment='限制的方式,0为不限制,1为活动期间限制,2为每天限制'),
    sa.Column('limit_num', sa.SmallInteger(), nullable=True, comment='限制的次数'),
    sa.Column('can_comment', sa.Boolean(), nullable=True, comment='投票后是否支持评论, 默认不支持'),
    sa.Column('vote_activity_type', sa.SmallInteger(), nullable=True, comment='投票后的游戏, 0为没有活动, 1为抽奖活动, 2为答题有奖, 3为玩游戏有奖'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_activity_manage_activity_name'), 'vote_activity_manage', ['activity_name'], unique=False)
    op.create_index(op.f('ix_vote_activity_manage_change_by_id'), 'vote_activity_manage', ['change_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_manage_create_by_id'), 'vote_activity_manage', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_manage_deleted_by_id'), 'vote_activity_manage', ['deleted_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_manage_state'), 'vote_activity_manage', ['state'], unique=False)
    op.create_table('vote_activity_option',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('change_by_id', sa.BigInteger(), nullable=True, comment='最后修改者ID'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('deleted_by_id', sa.BigInteger(), nullable=True, comment='删除者id'),
    sa.Column('player_name', sa.String(length=100), nullable=False, comment='选手姓名'),
    sa.Column('player_img', sa.String(length=300), nullable=False, comment='选手图片'),
    sa.Column('player_comment', sa.Text(), nullable=False, comment='选手介绍'),
    sa.Column('player_speech', sa.String(length=100), nullable=True, comment='选手感言'),
    sa.Column('activity_id', sa.String(length=20), nullable=False, comment='投票活动ID'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_activity_option_activity_id'), 'vote_activity_option', ['activity_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_option_change_by_id'), 'vote_activity_option', ['change_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_option_create_by_id'), 'vote_activity_option', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_option_deleted_by_id'), 'vote_activity_option', ['deleted_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_option_player_name'), 'vote_activity_option', ['player_name'], unique=False)
    op.create_index(op.f('ix_vote_activity_option_state'), 'vote_activity_option', ['state'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vote_activity_option_state'), table_name='vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_option_player_name'), table_name='vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_option_deleted_by_id'), table_name='vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_option_create_by_id'), table_name='vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_option_change_by_id'), table_name='vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_option_activity_id'), table_name='vote_activity_option')
    op.drop_table('vote_activity_option')
    op.drop_index(op.f('ix_vote_activity_manage_state'), table_name='vote_activity_manage')
    op.drop_index(op.f('ix_vote_activity_manage_deleted_by_id'), table_name='vote_activity_manage')
    op.drop_index(op.f('ix_vote_activity_manage_create_by_id'), table_name='vote_activity_manage')
    op.drop_index(op.f('ix_vote_activity_manage_change_by_id'), table_name='vote_activity_manage')
    op.drop_index(op.f('ix_vote_activity_manage_activity_name'), table_name='vote_activity_manage')
    op.drop_table('vote_activity_manage')
    # ### end Alembic commands ###
