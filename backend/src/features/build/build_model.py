from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape

from src.database import Base
from ...common.mixins.timestamp_mixin import TimestampMixin


class Build(TimestampMixin, Base):
    __tablename__ = "build"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    location = Column(Geography(geometry_type="POINT", srid=4326))
    organizations = relationship("Organization", back_populates="build")

    def set_location(self, latitude: float, longitude: float):
        self.location = f"POINT({longitude} {latitude})"

    def get_lat_lon(self):
        point = to_shape(self.location)
        return point.y, point.x
