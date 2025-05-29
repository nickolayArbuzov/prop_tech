from pydantic import BaseModel, Field
from datetime import datetime


class Organization(BaseModel):
    id: int
    name: str
    build_id: int

    class Config:
        orm_mode = True
