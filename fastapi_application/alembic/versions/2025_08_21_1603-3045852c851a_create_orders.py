"""create orders

Revision ID: 3045852c851a
Revises: eda79884a2ec
Create Date: 2025-08-21 16:03:33.450239

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3045852c851a"
down_revision: Union[str, Sequence[str], None] = "eda79884a2ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["users.id"],
            name=op.f("fk_orders_customer_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["statuses.id"],
            name=op.f("fk_orders_status_id_statuses"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders")
