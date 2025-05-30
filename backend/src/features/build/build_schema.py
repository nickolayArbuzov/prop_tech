from pydantic import BaseModel


class BuildInDB(BaseModel):
    address: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class ResponseBuild(BuildInDB):
    id: int
