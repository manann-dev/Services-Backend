"""token table created

Revision ID: 093bac04d128
Revises: 829eef7078d6
Create Date: 2024-02-26 14:47:29.961575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '093bac04d128'
down_revision: Union[str, None] = '829eef7078d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'response_type',
               existing_type=postgresql.ENUM('text', 'number', 'choice', name='response_type'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'response_type',
               existing_type=postgresql.ENUM('text', 'number', 'choice', name='response_type'),
               nullable=False)
    # ### end Alembic commands ###
