"""create products

Revision ID: 5b7e33a89862
Revises: a24d38dbf502
Create Date: 2025-08-21 14:31:38.582808

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5b7e33a89862"
down_revision: Union[str, Sequence[str], None] = "a24d38dbf502"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("describe", sa.String(), nullable=True),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("price_per_unit", sa.Integer(), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["supplier_id"],
            ["users.id"],
            name=op.f("fk_products_supplier_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")
