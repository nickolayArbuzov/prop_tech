from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
from src.database import Base
from src.features.organization.organization_model import organization_activity
from src.common.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from src.features.organization.organization_model import Organization
    from src.features.activity.activity_model import Activity


class Activity(TimestampMixin, Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activity.id"), nullable=True
    )
    parent: Mapped[Optional[Activity]] = relationship(
        "Activity",
        remote_side=[id],
        backref=backref("children", lazy="joined"),
    )

    organizations: Mapped[list[Organization]] = relationship(
        secondary=organization_activity, back_populates="activities"
    )
