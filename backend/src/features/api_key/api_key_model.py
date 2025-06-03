from __future__ import annotations

import uuid
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.common.mixins.timestamp_mixin import TimestampMixin
from src.database import Base


class APIKey(TimestampMixin, Base):
    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
