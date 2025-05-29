from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class Filters(BaseModel):
    name: Optional[str] = None


def get_filters(
    name: Optional[str] = Query(
        None, min_length=1, description="Name of organization to search"
    )
) -> Filters:
    return Filters(name=name)
