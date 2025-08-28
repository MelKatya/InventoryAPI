"""unique users roles

Revision ID: 7546d8736a7a
Revises: d81dc0f79668
Create Date: 2025-08-28 21:23:36.943789

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7546d8736a7a"
down_revision: Union[str, Sequence[str], None] = "d81dc0f79668"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        op.f("uq_users_roles_user_id"), "users_roles", ["user_id", "role_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("uq_users_roles_user_id"), "users_roles", type_="unique"
    )

