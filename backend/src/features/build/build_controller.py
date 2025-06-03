from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .build_schema import ResponseBuild
from src.dependencies import get_read_db, verify_api_key
from .usecases.query import GetManyUseCase, GetManyQuery
from .repositories import BuildQueryRepository
from src.common import Pagination, WithPaginationResponse

router = APIRouter()


@router.get("/builds", response_model=WithPaginationResponse[ResponseBuild])
async def get_many(
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    _api_key=Depends(verify_api_key),
):
    build_query_repository = BuildQueryRepository(db)
    query = GetManyQuery(pagination=pagination)
    use_case = GetManyUseCase(build_repository=build_query_repository)
    return await use_case.execute(query)
