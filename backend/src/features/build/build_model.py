from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography

from src.database import Base
from src.common.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from src.features.organization.organization_model import Organization


class Build(TimestampMixin, Base):
    __tablename__ = "build"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column()
    location: Mapped[Geography] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )

    organizations: Mapped[list[Organization]] = relationship(back_populates="build")
