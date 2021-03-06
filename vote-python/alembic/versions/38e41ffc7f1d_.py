"""empty message

Revision ID: 38e41ffc7f1d
Revises: 9ef6b6912874
Create Date: 2020-08-20 22:40:32.037108

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '38e41ffc7f1d'
down_revision = '9ef6b6912874'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote_activity_player',
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
    sa.Column('support_vote_num', sa.Integer(), nullable=True, comment='支持的投票数量'),
    sa.Column('against_vote_num', sa.Integer(), nullable=True, comment='反对的投票数量'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_activity_player_activity_id'), 'vote_activity_player', ['activity_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_player_change_by_id'), 'vote_activity_player', ['change_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_player_create_by_id'), 'vote_activity_player', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_player_deleted_by_id'), 'vote_activity_player', ['deleted_by_id'], unique=False)
    op.create_index(op.f('ix_vote_activity_player_player_name'), 'vote_activity_player', ['player_name'], unique=False)
    op.create_index(op.f('ix_vote_activity_player_state'), 'vote_activity_player', ['state'], unique=False)
    op.create_table('vote_comment_support',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID,即关注者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('comment_id', sa.String(length=20), nullable=False, comment='评论id'),
    sa.Column('subscriber_id', sa.String(length=20), nullable=False, comment='点赞者id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_comment_support_comment_id'), 'vote_comment_support', ['comment_id'], unique=False)
    op.create_index(op.f('ix_vote_comment_support_create_by_id'), 'vote_comment_support', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_comment_support_state'), 'vote_comment_support', ['state'], unique=False)
    op.create_index(op.f('ix_vote_comment_support_subscriber_id'), 'vote_comment_support', ['subscriber_id'], unique=False)
    op.create_table('vote_luck_draw_gift',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('change_by_id', sa.BigInteger(), nullable=True, comment='最后修改者ID'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('deleted_by_id', sa.BigInteger(), nullable=True, comment='删除者id'),
    sa.Column('activity_id', sa.String(length=20), nullable=False, comment='投票活动ID'),
    sa.Column('gift_name', sa.String(length=100), nullable=False, comment='奖品名称'),
    sa.Column('gift_img', sa.String(length=300), nullable=True, comment='奖品相片'),
    sa.Column('winning_chance', sa.Float(), nullable=False, comment='中奖几率'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_luck_draw_gift_activity_id'), 'vote_luck_draw_gift', ['activity_id'], unique=False)
    op.create_index(op.f('ix_vote_luck_draw_gift_change_by_id'), 'vote_luck_draw_gift', ['change_by_id'], unique=False)
    op.create_index(op.f('ix_vote_luck_draw_gift_create_by_id'), 'vote_luck_draw_gift', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_luck_draw_gift_deleted_by_id'), 'vote_luck_draw_gift', ['deleted_by_id'], unique=False)
    op.create_index(op.f('ix_vote_luck_draw_gift_state'), 'vote_luck_draw_gift', ['state'], unique=False)
    op.create_table('vote_player_comment',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID,即关注者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('player_id', sa.String(length=20), nullable=False, comment='选手ID'),
    sa.Column('parent_id', sa.String(length=20), nullable=True, comment='评论者id自关联'),
    sa.Column('support_or_against', sa.Boolean(), nullable=True, comment='支持还是反对'),
    sa.Column('comment', sa.String(length=150), nullable=False, comment='评论'),
    sa.Column('support_num', sa.Integer(), nullable=True, comment='点赞数'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_player_comment_create_by_id'), 'vote_player_comment', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_player_comment_player_id'), 'vote_player_comment', ['player_id'], unique=False)
    op.create_index(op.f('ix_vote_player_comment_state'), 'vote_player_comment', ['state'], unique=False)
    op.create_table('vote_subscriber_gift',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False, comment='主键ID'),
    sa.Column('state', sa.SmallInteger(), nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', sa.BigInteger(), nullable=True, comment='创建者ID,即关注者ID'),
    sa.Column('last_change_time', sa.DateTime(), nullable=True, comment='最后修改的时间'),
    sa.Column('deleted_time', sa.DateTime(), nullable=True, comment='删除时间'),
    sa.Column('gift_id', sa.String(length=20), nullable=False, comment='奖品ID'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_vote_subscriber_gift_create_by_id'), 'vote_subscriber_gift', ['create_by_id'], unique=False)
    op.create_index(op.f('ix_vote_subscriber_gift_gift_id'), 'vote_subscriber_gift', ['gift_id'], unique=False)
    op.create_index(op.f('ix_vote_subscriber_gift_state'), 'vote_subscriber_gift', ['state'], unique=False)
    op.drop_index('id', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_activity_id', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_change_by_id', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_create_by_id', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_deleted_by_id', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_player_name', table_name='vote_activity_option')
    op.drop_index('ix_vote_activity_option_state', table_name='vote_activity_option')
    op.drop_table('vote_activity_option')
    op.add_column('vote_activity_manage', sa.Column('against_vote_num', sa.Integer(), nullable=True, comment='反对的投票数量'))
    op.add_column('vote_activity_manage', sa.Column('comment_before_lucky_draw', sa.Boolean(), nullable=True, comment='先评论后抽奖或先抽奖再评论'))
    op.add_column('vote_activity_manage', sa.Column('lottery_limit', sa.Boolean(), nullable=True, comment='是否限制'))
    op.add_column('vote_activity_manage', sa.Column('lottery_num', sa.SmallInteger(), nullable=True, comment='一次投票活动用户中奖后是否还可以抽奖'))
    op.add_column('vote_activity_manage', sa.Column('lucky_draw_remarks', sa.String(length=100), nullable=True, comment='抽奖备注'))
    op.add_column('vote_activity_manage', sa.Column('support_vote_num', sa.Integer(), nullable=True, comment='支持的投票数量'))
    op.alter_column('vote_activity_manage', 'limit_num',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='对单用户限制的投票次数',
               existing_comment='限制的次数',
               existing_nullable=True)
    op.alter_column('vote_activity_manage', 'limit_type',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='限制的方式,0为不限制,1为对账号限制,2为每天限制',
               existing_comment='限制的方式,0为不限制,1为活动期间限制,2为每天限制',
               existing_nullable=True)
    op.alter_column('vote_activity_manage', 'vote_activity_type',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='投票后的游戏, 0为没有活动, 1为大转盘抽奖, 2为九宫格抽奖, 3为刮刮乐抽奖, 4为答题有奖, 5为玩游戏有奖',
               existing_comment='投票后的游戏, 0为没有活动, 1为抽奖活动, 2为答题有奖, 3为玩游戏有奖',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vote_activity_manage', 'vote_activity_type',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='投票后的游戏, 0为没有活动, 1为抽奖活动, 2为答题有奖, 3为玩游戏有奖',
               existing_comment='投票后的游戏, 0为没有活动, 1为大转盘抽奖, 2为九宫格抽奖, 3为刮刮乐抽奖, 4为答题有奖, 5为玩游戏有奖',
               existing_nullable=True)
    op.alter_column('vote_activity_manage', 'limit_type',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='限制的方式,0为不限制,1为活动期间限制,2为每天限制',
               existing_comment='限制的方式,0为不限制,1为对账号限制,2为每天限制',
               existing_nullable=True)
    op.alter_column('vote_activity_manage', 'limit_num',
               existing_type=mysql.SMALLINT(display_width=6),
               comment='限制的次数',
               existing_comment='对单用户限制的投票次数',
               existing_nullable=True)
    op.drop_column('vote_activity_manage', 'support_vote_num')
    op.drop_column('vote_activity_manage', 'lucky_draw_remarks')
    op.drop_column('vote_activity_manage', 'lottery_num')
    op.drop_column('vote_activity_manage', 'lottery_limit')
    op.drop_column('vote_activity_manage', 'comment_before_lucky_draw')
    op.drop_column('vote_activity_manage', 'against_vote_num')
    op.create_table('vote_activity_option',
    sa.Column('id', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False, comment='主键ID'),
    sa.Column('state', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True, comment='状态值, 0为已删除, 1为正常, 2为锁定'),
    sa.Column('create_time', mysql.DATETIME(), nullable=False, comment='创建时间'),
    sa.Column('create_by_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True, comment='创建者ID'),
    sa.Column('last_change_time', mysql.DATETIME(), nullable=True, comment='最后修改的时间'),
    sa.Column('change_by_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True, comment='最后修改者ID'),
    sa.Column('deleted_time', mysql.DATETIME(), nullable=True, comment='删除时间'),
    sa.Column('deleted_by_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True, comment='删除者id'),
    sa.Column('player_name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=False, comment='选手姓名'),
    sa.Column('player_img', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=300), nullable=False, comment='选手图片'),
    sa.Column('player_comment', mysql.TEXT(collation='utf8mb4_unicode_ci'), nullable=False, comment='选手介绍'),
    sa.Column('player_speech', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=True, comment='选手感言'),
    sa.Column('activity_id', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False, comment='投票活动ID'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_vote_activity_option_state', 'vote_activity_option', ['state'], unique=False)
    op.create_index('ix_vote_activity_option_player_name', 'vote_activity_option', ['player_name'], unique=False)
    op.create_index('ix_vote_activity_option_deleted_by_id', 'vote_activity_option', ['deleted_by_id'], unique=False)
    op.create_index('ix_vote_activity_option_create_by_id', 'vote_activity_option', ['create_by_id'], unique=False)
    op.create_index('ix_vote_activity_option_change_by_id', 'vote_activity_option', ['change_by_id'], unique=False)
    op.create_index('ix_vote_activity_option_activity_id', 'vote_activity_option', ['activity_id'], unique=False)
    op.create_index('id', 'vote_activity_option', ['id'], unique=True)
    op.drop_index(op.f('ix_vote_subscriber_gift_state'), table_name='vote_subscriber_gift')
    op.drop_index(op.f('ix_vote_subscriber_gift_gift_id'), table_name='vote_subscriber_gift')
    op.drop_index(op.f('ix_vote_subscriber_gift_create_by_id'), table_name='vote_subscriber_gift')
    op.drop_table('vote_subscriber_gift')
    op.drop_index(op.f('ix_vote_player_comment_state'), table_name='vote_player_comment')
    op.drop_index(op.f('ix_vote_player_comment_player_id'), table_name='vote_player_comment')
    op.drop_index(op.f('ix_vote_player_comment_create_by_id'), table_name='vote_player_comment')
    op.drop_table('vote_player_comment')
    op.drop_index(op.f('ix_vote_luck_draw_gift_state'), table_name='vote_luck_draw_gift')
    op.drop_index(op.f('ix_vote_luck_draw_gift_deleted_by_id'), table_name='vote_luck_draw_gift')
    op.drop_index(op.f('ix_vote_luck_draw_gift_create_by_id'), table_name='vote_luck_draw_gift')
    op.drop_index(op.f('ix_vote_luck_draw_gift_change_by_id'), table_name='vote_luck_draw_gift')
    op.drop_index(op.f('ix_vote_luck_draw_gift_activity_id'), table_name='vote_luck_draw_gift')
    op.drop_table('vote_luck_draw_gift')
    op.drop_index(op.f('ix_vote_comment_support_subscriber_id'), table_name='vote_comment_support')
    op.drop_index(op.f('ix_vote_comment_support_state'), table_name='vote_comment_support')
    op.drop_index(op.f('ix_vote_comment_support_create_by_id'), table_name='vote_comment_support')
    op.drop_index(op.f('ix_vote_comment_support_comment_id'), table_name='vote_comment_support')
    op.drop_table('vote_comment_support')
    op.drop_index(op.f('ix_vote_activity_player_state'), table_name='vote_activity_player')
    op.drop_index(op.f('ix_vote_activity_player_player_name'), table_name='vote_activity_player')
    op.drop_index(op.f('ix_vote_activity_player_deleted_by_id'), table_name='vote_activity_player')
    op.drop_index(op.f('ix_vote_activity_player_create_by_id'), table_name='vote_activity_player')
    op.drop_index(op.f('ix_vote_activity_player_change_by_id'), table_name='vote_activity_player')
    op.drop_index(op.f('ix_vote_activity_player_activity_id'), table_name='vote_activity_player')
    op.drop_table('vote_activity_player')
    # ### end Alembic commands ###
