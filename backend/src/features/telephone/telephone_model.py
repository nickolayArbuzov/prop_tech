from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base
from src.common.mixins.timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from src.features.organization.organization_model import Organization


class Telephone(TimestampMixin, Base):
    __tablename__ = "telephone"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column()
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    organization: Mapped[Organization] = relationship(back_populates="telephones")
