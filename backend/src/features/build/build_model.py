from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship

from src.database import Base

from ...common.mixins.timestamp_mixin import TimestampMixin

class Build(TimestampMixin, Base):
    __tablename__ = 'build'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    organizations = relationship('Organization', back_populates='build')

