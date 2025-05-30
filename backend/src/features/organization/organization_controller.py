from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_read_db
from .usecases.query import (
    GetManyByBuildingUseCase,
    GetManyByBuildingQuery,
    GetManyByActivityUseCase,
    GetManyByActivityQuery,
    GetManyByGeoUseCase,
    GetManyByGeoQuery,
    GetOneByIdUseCase,
    GetOneByIdQuery,
    GetManyByActivityAllUseCase,
    GetManyByActivityAllQuery,
    GetByNameUseCase,
    GetByNameQuery,
)
from .repositories import OrganizationQueryRepository
from .organization_swagger import (
    getManyByBuildingDoc,
    getManyByActivityDoc,
    getManyByGeoDoc,
    getOneByIdDoc,
    getManyByActivityAllDoc,
    getByNameDoc,
)
from src.common import FilterByName, FilterByLocation, Pagination

router = APIRouter()


@router.get("/organizations/by-building/{building_id}", responses=getManyByBuildingDoc)
async def getManyByBuilding(
    building_id: int,
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByBuildingQuery(building_id=building_id, pagination=pagination)
    use_case = GetManyByBuildingUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get("/organizations/by-activity/{activity_id}", responses=getManyByActivityDoc)
async def getManyByActivity(
    activity_id: int,
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityQuery(activity_id=activity_id, pagination=pagination)
    use_case = GetManyByActivityUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get("/organizations/by-geolocation", responses=getManyByGeoDoc)
async def getManyByGeolocation(
    db: AsyncSession = Depends(get_read_db), location: FilterByLocation = Depends()
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByGeoQuery(location=location)
    use_case = GetManyByGeoUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get(
    "/organizations/by-activity-tree/{activity_id}", responses=getManyByActivityAllDoc
)
async def getManyByActivityTree(
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityAllQuery(pagination=pagination)
    use_case = GetManyByActivityAllUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get("/organizations/search", responses=getByNameDoc)
async def getByName(
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    filters: FilterByName = Depends(),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetByNameQuery(pagination=pagination, filters=filters)
    use_case = GetByNameUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)


@router.get("/organizations/{organization_id}", responses=getOneByIdDoc)
async def getOneById(organization_id: int, db: AsyncSession = Depends(get_read_db)):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetOneByIdQuery(organization_id=organization_id)
    use_case = GetOneByIdUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)
