"""added base tables

Revision ID: 990c6446a8f6
Revises: 
Create Date: 2021-09-12 14:41:59.870981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '990c6446a8f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rubric',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rubric')
    op.drop_table('documents')
    # ### end Alembic commands ###
