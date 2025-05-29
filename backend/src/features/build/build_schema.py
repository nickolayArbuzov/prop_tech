from pydantic import BaseModel, Field
from datetime import datetime



class Build(BaseModel):
    id: int
    address: str
    latitude: str
    longitude: str
    class Config:
        orm_mode = True
