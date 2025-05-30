from pydantic import BaseModel

from src.features.telephone.telephone_schema import ResponseTelephone
from src.features.activity.activity_schema import ResponseActivity
from src.features.build.build_schema import ResponseBuild


class OrganizationInDB(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ResponseOrganization(OrganizationInDB):
    id: int


class OrganizationDetail(ResponseOrganization):
    telephones: list[ResponseTelephone]
    activities: list[ResponseActivity]
    build: ResponseBuild
