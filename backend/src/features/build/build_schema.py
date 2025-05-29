from pydantic import BaseModel


class Build(BaseModel):
    id: int
    address: str
    latitude: str
    longitude: str

    class Config:
        orm_mode = True
