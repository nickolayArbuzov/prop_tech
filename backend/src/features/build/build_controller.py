from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_read_db
from .usecases.query import GetManyUseCase, GetManyQuery
from .repositories import BuildQueryRepository
from .build_swagger import getManyDoc
from src.common.pagination import Pagination

router = APIRouter()

@router.get("/builds", responses=getManyDoc)
async def getMany(db: AsyncSession = Depends(get_read_db), pagination: Pagination = Depends()):
    build_query_repository = BuildQueryRepository(db)
    query = GetManyQuery(pagination=pagination)
    use_case = GetManyUseCase(build_repository=build_query_repository)
    return await use_case.execute(query)


