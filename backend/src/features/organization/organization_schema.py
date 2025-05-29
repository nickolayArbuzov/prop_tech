from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    name: str
    build_id: int

    class Config:
        orm_mode = True
