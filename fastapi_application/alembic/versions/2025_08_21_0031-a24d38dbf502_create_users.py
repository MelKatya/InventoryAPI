"""create users

Revision ID: a24d38dbf502
Revises: a8e76bfed05e
Create Date: 2025-08-21 00:31:40.443875

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a24d38dbf502"
down_revision: Union[str, Sequence[str], None] = "a8e76bfed05e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("id_role", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_role"], ["roles.id"], name=op.f("fk_users_id_role_roles")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
