"""create users_roles

Revision ID: d81dc0f79668
Revises: 29377118d4fc
Create Date: 2025-08-21 18:20:53.953563

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d81dc0f79668"
down_revision: Union[str, Sequence[str], None] = "29377118d4fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users_roles",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk_users_roles_role_id_roles"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_users_roles_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "role_id", name=op.f("pk_users_roles")
        ),
        sa.UniqueConstraint(
            "user_id", "role_id", name=op.f("uq_users_roles_user_id")
        ),
    )
    op.drop_constraint(
        op.f("fk_users_id_role_roles"), "users", type_="foreignkey"
    )
    op.drop_column("users", "id_role")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "id_role", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        op.f("fk_users_id_role_roles"), "users", "roles", ["id_role"], ["id"]
    )
    op.drop_table("users_roles")

