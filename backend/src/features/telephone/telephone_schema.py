from pydantic import BaseModel


class TelephoneInDB(BaseModel):
    phone_number: str

    class Config:
        orm_mode = True


class ResponseTelephone(TelephoneInDB):
    id: int
