from pydantic import BaseModel


class Activity(BaseModel):
    id: int
    name: str
    organization_id: int

    class Config:
        orm_mode = True
