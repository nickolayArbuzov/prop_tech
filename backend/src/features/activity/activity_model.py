from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship, backref

from src.database import Base
from src.features.organization.organization_model import organization_activity
from src.common.mixins.timestamp_mixin import TimestampMixin


class Activity(TimestampMixin, Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activity.id"), nullable=True)
    parent = relationship(
        "Activity", remote_side=[id], backref=backref("children", lazy="joined")
    )
    organizations = relationship(
        "Organization", secondary=organization_activity, back_populates="activities"
    )
