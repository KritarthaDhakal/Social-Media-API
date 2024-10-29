"""changes?

Revision ID: c8e27784443c
Revises: 02d568d5cd3c
Create Date: 2024-01-02 02:49:53.285103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e27784443c'
down_revision: Union[str, None] = '02d568d5cd3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
