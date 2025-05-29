from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from src.database import Base

from ...common.mixins.timestamp_mixin import TimestampMixin
organization_activity = Table(
    'organization_activity', Base.metadata,
    Column('organization_id', ForeignKey('organization.id')),
    Column('activity_id', ForeignKey('activity.id'))
)

class Organization(TimestampMixin, Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    telephones = relationship('Telephone', back_populates='organization')
    build_id = Column(Integer, ForeignKey('build.id'))
    build = relationship('Build', back_populates='organizations')
    activities = relationship('Activity', secondary=organization_activity, back_populates='organizations')

