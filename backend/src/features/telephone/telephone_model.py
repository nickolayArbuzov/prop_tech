from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship

from src.database import Base

from ...common.mixins.timestamp_mixin import TimestampMixin

class Telephone(TimestampMixin, Base):
    __tablename__ = 'telephone'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String)

    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', back_populates='telephones')

