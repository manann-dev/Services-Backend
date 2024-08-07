"""updated field in token

Revision ID: 68170246a3a5
Revises: eb3d881536f6
Create Date: 2024-02-27 13:39:53.516519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68170246a3a5'
down_revision: Union[str, None] = 'eb3d881536f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'refresh_token',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=1000),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'refresh_token',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###
