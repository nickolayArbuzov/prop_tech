"""create init migration

Revision ID: 248dd87e5dc2
Revises:
Create Date: 2025-05-29 21:18:36.641312

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "248dd87e5dc2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "api_key",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "key",
            postgresql.UUID(as_uuid=True),
            default=uuid.uuid4,
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "build",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("address", sa.String()),
        sa.Column("location", Geography(geometry_type="POINT", srid=4326)),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_build_location", "build", ["location"], postgresql_using="gist")

    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String()),
        sa.Column("build_id", sa.Integer(), sa.ForeignKey("build.id")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_organization_build_id", "organization", ["build_id"])
    op.create_index("ix_organization_name", "organization", ["name"])

    op.create_table(
        "telephone",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("phone_number", sa.String()),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organization.id")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_telephone_organization_id", "telephone", ["organization_id"])

    op.create_table(
        "activity",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "parent_id", sa.Integer(), sa.ForeignKey("activity.id"), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_activity_parent_id", "activity", ["parent_id"])

    op.create_table(
        "organization_activity",
        sa.Column(
            "organization_id",
            sa.Integer(),
            sa.ForeignKey("organization.id"),
            primary_key=True,
        ),
        sa.Column(
            "activity_id", sa.Integer(), sa.ForeignKey("activity.id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("api_key")
    op.drop_table("organization_activity")
    op.drop_index("ix_activity_parent_id", table_name="activity")
    op.drop_table("activity")
    op.drop_index("ix_telephone_organization_id", table_name="telephone")
    op.drop_table("telephone")
    op.drop_index("ix_organization_build_id", table_name="organization")
    op.drop_index("ix_organization_name", table_name="organization")
    op.drop_table("organization")
    op.drop_index("ix_build_location", table_name="build")
    op.drop_table("build")
