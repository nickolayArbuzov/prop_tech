from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship

from src.database import Base

from ...common.mixins.timestamp_mixin import TimestampMixin

class Activity(TimestampMixin, Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


