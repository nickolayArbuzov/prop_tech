from pydantic import BaseModel


class Telephone(BaseModel):
    id: int
    phone_number: str
    organization_id: int

    class Config:
        orm_mode = True
