"""Create incidents table.

Revision ID: 001
Revises:
Create Date: 2026-04-15
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "incidents",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("reporter_email", sa.String(255), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "submitted", "triaging", "triaged", "dispatched", "resolved", "blocked",
                name="incidentstatus",
            ),
            nullable=False,
            server_default="submitted",
        ),
        sa.Column(
            "severity",
            sa.Enum("P0", "P1", "P2", "P3", "P4", "unknown", name="incidentseverity"),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column("attachments", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("triage_result", postgresql.JSONB(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("cost_usd", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("incidents")
    op.execute("DROP TYPE IF EXISTS incidentstatus")
    op.execute("DROP TYPE IF EXISTS incidentseverity")
