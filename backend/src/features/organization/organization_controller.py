from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_read_db
from .usecases.query import GetManyByBuildingUseCase, GetManyByBuildingQuery, GetManyByActivityUseCase, GetManyByActivityQuery, GetManyByGeoUseCase, GetManyByGeoQuery, GetOneByIdUseCase, GetOneByIdQuery, GetManyByActivityAllUseCase, GetManyByActivityAllQuery, GetByNameUseCase, GetByNameQuery
from .repositories import OrganizationQueryRepository
from .organization_swagger import getManyByBuildingDoc, getManyByActivityDoc, getManyByGeoDoc, getOneByIdDoc, getManyByActivityAllDoc, getByNameDoc
from src.common.pagination import Pagination

router = APIRouter()

@router.get("/organizations", responses=getManyByBuildingDoc)
async def getManyByBuilding(db: AsyncSession = Depends(get_read_db), pagination: Pagination = Depends()):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByBuildingQuery(pagination=pagination)
    use_case = GetManyByBuildingUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organizations", responses=getManyByActivityDoc)
async def getManyByActivity(db: AsyncSession = Depends(get_read_db), pagination: Pagination = Depends()):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityQuery(pagination=pagination)
    use_case = GetManyByActivityUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organizations", responses=getManyByGeoDoc)
async def getManyByGeo(db: AsyncSession = Depends(get_read_db)):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByGeoQuery()
    use_case = GetManyByGeoUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organization/{organization_id}/telephones/activities", responses=getOneByIdDoc)
async def getOneById(organization_id: int, db: AsyncSession = Depends(get_read_db)):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetOneByIdQuery(organization_id=organization_id)
    use_case = GetOneByIdUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organizations", responses=getManyByActivityAllDoc)
async def getManyByActivityAll(db: AsyncSession = Depends(get_read_db), pagination: Pagination = Depends()):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityAllQuery(pagination=pagination)
    use_case = GetManyByActivityAllUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organization/{organization_id}", responses=getByNameDoc)
async def getByName(organization_id: int, db: AsyncSession = Depends(get_read_db)):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetByNameQuery(organization_id=organization_id)
    use_case = GetByNameUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


