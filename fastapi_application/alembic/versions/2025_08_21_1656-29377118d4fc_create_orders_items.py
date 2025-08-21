"""create orders_items

Revision ID: 29377118d4fc
Revises: 3045852c851a
Create Date: 2025-08-21 16:56:41.708238

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "29377118d4fc"
down_revision: Union[str, Sequence[str], None] = "3045852c851a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "orders_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price_at_moment", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_orders_items_order_id_orders"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_orders_items_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders_items")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders_items")
