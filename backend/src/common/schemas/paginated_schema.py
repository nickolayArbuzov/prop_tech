from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class BasePaginatedResponse(GenericModel, Generic[T]):
    data: list[T]
    total: int


class WithTotalCountResponse(BasePaginatedResponse[T]):
    pass


class WithPaginationResponse(BasePaginatedResponse[T]):
    page: int
    limit: int
