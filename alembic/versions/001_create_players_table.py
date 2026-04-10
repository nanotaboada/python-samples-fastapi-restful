"""Create players table

Revision ID: 001
Revises:
Create Date: 2026-04-09

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("firstName", sa.String(), nullable=False),
        sa.Column("middleName", sa.String(), nullable=True),
        sa.Column("lastName", sa.String(), nullable=False),
        sa.Column("dateOfBirth", sa.String(), nullable=True),
        sa.Column("squadNumber", sa.Integer(), nullable=False),
        sa.Column("position", sa.String(), nullable=False),
        sa.Column("abbrPosition", sa.String(), nullable=True),
        sa.Column("team", sa.String(), nullable=True),
        sa.Column("league", sa.String(), nullable=True),
        sa.Column("starting11", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("squadNumber"),
    )


def downgrade() -> None:
    op.drop_table("players")
