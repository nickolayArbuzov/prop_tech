from typing import Optional
from pydantic import BaseModel, Field


class FilterByName(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, description="Organization name to search"
    )


class FilterByLocation(BaseModel):
    latitude: Optional[float] = Field(None, description="Latitude in WGS84")
    longitude: Optional[float] = Field(None, description="Longitude in WGS84")
    radius: Optional[float] = Field(None, gt=0, description="Search radius in meters")
