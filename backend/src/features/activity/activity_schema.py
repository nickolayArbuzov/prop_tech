from pydantic import BaseModel


class ActivityInDB(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ResponseActivity(ActivityInDB):
    id: int
