"""create status

Revision ID: eda79884a2ec
Revises: 5b7e33a89862
Create Date: 2025-08-21 15:46:10.995304

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eda79884a2ec"
down_revision: Union[str, Sequence[str], None] = "5b7e33a89862"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    statuses_table = op.create_table(
        "statuses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_statuses")),
    )
    op.bulk_insert(statuses_table, [
        {"name": "new"},
        {"name": "confirmed"},
        {"name": "cancelled"},
        {"name": "shipped"},
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("statuses")
