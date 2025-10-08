"""Add sensor tables

Revision ID: 2f0d3934c87b
Revises: 1ebced84321d
Create Date: 2025-10-08 17:38:16.922151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f0d3934c87b'
down_revision: Union[str, Sequence[str], None] = '1ebced84321d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "sensortype",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("unit", sa.String()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sensortype_name", "sensortype", ["name"], unique=True)

    op.create_table(
        "sensor",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["device.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["sensortype.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sensor_name", "sensor", ["name"])


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index("ix_sensor_name", table_name="sensor")
    op.drop_table("sensor")

    op.drop_index("ix_sensortype_name", table_name="sensortype")
    op.drop_table("sensortype")
