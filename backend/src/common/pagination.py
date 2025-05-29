from pydantic import BaseModel
from fastapi import Query


class Pagination(BaseModel):
    page: int = 1
    limit: int = 10


def get_pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
) -> Pagination:
    return Pagination(page=page, limit=limit)
