from pydantic import BaseModel, Field
from datetime import datetime



class Activity(BaseModel):
    id: int
    name: str
    organization_id: int

    class Config:
        orm_mode = True
