"""empty message

Revision ID: 2c69acde2f0b
Revises: bca34c909afb
Create Date: 2021-02-04 16:01:43.293225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c69acde2f0b'
down_revision = 'bca34c909afb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fund_shares_rel',
    sa.Column('rel_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('fund_no', sa.String(length=10), nullable=False, comment='基金代码'),
    sa.Column('shares_no', sa.String(length=10), nullable=False, comment='股票代码'),
    sa.PrimaryKeyConstraint('rel_id'),
    sa.UniqueConstraint('rel_id'),
    comment='基金股票关联表'
    )
    op.create_index(op.f('ix_fund_shares_rel_fund_no'), 'fund_shares_rel', ['fund_no'], unique=False)
    op.create_index(op.f('ix_fund_shares_rel_shares_no'), 'fund_shares_rel', ['shares_no'], unique=False)
    op.create_table('shares_date_info',
    sa.Column('date_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('shares_no', sa.String(length=10), nullable=False, comment='股票代码'),
    sa.Column('unit_date', sa.Date(), nullable=False, comment='单位日期'),
    sa.Column('now_price', sa.FLOAT(), nullable=True, comment='当前价格'),
    sa.Column('date_up', sa.FLOAT(), nullable=True, comment='当日涨幅'),
    sa.Column('main_inflow', sa.FLOAT(), nullable=True, comment='主力净流入'),
    sa.Column('super_large_inflow', sa.FLOAT(), nullable=True, comment='超大单净流入'),
    sa.Column('large_inflow', sa.FLOAT(), nullable=True, comment='大单净流入'),
    sa.Column('middle_inflow', sa.FLOAT(), nullable=True, comment='中单净流入'),
    sa.Column('small_inflow', sa.FLOAT(), nullable=True, comment='小单净流入'),
    sa.PrimaryKeyConstraint('date_id'),
    sa.UniqueConstraint('date_id'),
    comment='股票日详情表'
    )
    op.create_index(op.f('ix_shares_date_info_shares_no'), 'shares_date_info', ['shares_no'], unique=False)
    op.create_index(op.f('ix_shares_date_info_unit_date'), 'shares_date_info', ['unit_date'], unique=False)
    op.create_table('shares_info',
    sa.Column('shares_no', sa.String(length=10), nullable=False, comment='股票代码'),
    sa.Column('shares_name', sa.String(length=100), nullable=False, comment='股票名称'),
    sa.PrimaryKeyConstraint('shares_no'),
    comment='股票表'
    )
    op.create_index(op.f('ix_shares_info_shares_name'), 'shares_info', ['shares_name'], unique=False)
    op.create_index(op.f('ix_shares_info_shares_no'), 'shares_info', ['shares_no'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shares_info_shares_no'), table_name='shares_info')
    op.drop_index(op.f('ix_shares_info_shares_name'), table_name='shares_info')
    op.drop_table('shares_info')
    op.drop_index(op.f('ix_shares_date_info_unit_date'), table_name='shares_date_info')
    op.drop_index(op.f('ix_shares_date_info_shares_no'), table_name='shares_date_info')
    op.drop_table('shares_date_info')
    op.drop_index(op.f('ix_fund_shares_rel_shares_no'), table_name='fund_shares_rel')
    op.drop_index(op.f('ix_fund_shares_rel_fund_no'), table_name='fund_shares_rel')
    op.drop_table('fund_shares_rel')
    # ### end Alembic commands ###