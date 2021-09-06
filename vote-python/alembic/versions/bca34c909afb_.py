"""empty message

Revision ID: bca34c909afb
Revises: 59a3c1b46e45
Create Date: 2021-02-03 15:32:58.669755

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bca34c909afb'
down_revision = '59a3c1b46e45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_fund_shares_rel_fund_no', table_name='fund_shares_rel')
    op.drop_index('ix_fund_shares_rel_shares_no', table_name='fund_shares_rel')
    op.drop_index('rel_id', table_name='fund_shares_rel')
    op.drop_table('fund_shares_rel')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fund_shares_rel',
    sa.Column('rel_id', mysql.BIGINT(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('fund_no', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=10), nullable=False, comment='基金代码'),
    sa.Column('shares_no', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=10), nullable=False, comment='股票代码'),
    sa.Column('proportion', mysql.FLOAT(), nullable=True, comment='当前持仓占比'),
    sa.Column('hold_change', mysql.FLOAT(), nullable=True, comment='持有变化, 0：不变, 整数：增持, 负数：减持'),
    sa.PrimaryKeyConstraint('rel_id'),
    comment='基金股票关系表',
    mysql_collate='utf8mb4_unicode_ci',
    mysql_comment='基金股票关系表',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB',
    mysql_row_format='DYNAMIC'
    )
    op.create_index('rel_id', 'fund_shares_rel', ['rel_id'], unique=True)
    op.create_index('ix_fund_shares_rel_shares_no', 'fund_shares_rel', ['shares_no'], unique=False)
    op.create_index('ix_fund_shares_rel_fund_no', 'fund_shares_rel', ['fund_no'], unique=False)
    # ### end Alembic commands ###