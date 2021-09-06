"""empty message

Revision ID: 1d4aed2f56a3
Revises: 24c4974b2941
Create Date: 2020-08-23 23:18:03.594553

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d4aed2f56a3'
down_revision = '24c4974b2941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vote_activity_manage', 'limit_vote')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vote_activity_manage', sa.Column('limit_vote', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='投票次数是否限制'))
    # ### end Alembic commands ###