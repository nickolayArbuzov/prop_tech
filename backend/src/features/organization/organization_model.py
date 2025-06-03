from __future__ import annotations

from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.common.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from src.features.telephone.telephone_model import Telephone
    from src.features.build.build_model import Build
    from src.features.activity.activity_model import Activity

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
)


class Organization(TimestampMixin, Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()

    build_id: Mapped[int] = mapped_column(ForeignKey("build.id"))
    build: Mapped[Build] = relationship(back_populates="organizations")

    telephones: Mapped[List[Telephone]] = relationship(back_populates="organization")

    activities: Mapped[List[Activity]] = relationship(
        secondary=organization_activity, back_populates="organizations"
    )
