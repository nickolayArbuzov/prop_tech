from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    limit: int = Query(10, ge=1, le=100, description="Number of entries per page")
