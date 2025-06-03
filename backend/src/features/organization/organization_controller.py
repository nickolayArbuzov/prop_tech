from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .organization_schema import ResponseOrganization, OrganizationDetail
from src.dependencies import get_read_db, verify_api_key
from .usecases.query import (
    GetManyByBuildingUseCase,
    GetManyByBuildingQuery,
    GetManyByActivityUseCase,
    GetManyByActivityQuery,
    GetManyByGeoUseCase,
    GetManyByGeoQuery,
    GetOneByIdUseCase,
    GetOneByIdQuery,
    GetManyByActivityTreeUseCase,
    GetManyByActivityTreeQuery,
    GetManyByNameUseCase,
    GetManyByNameQuery,
)
from .repositories import OrganizationQueryRepository
from src.common import (
    FilterByName,
    FilterByLocation,
    Pagination,
    WithPaginationResponse,
    WithTotalCountResponse,
)

router = APIRouter()


@router.get(
    "/organizations/by-building/{building_id}",
    response_model=WithPaginationResponse[ResponseOrganization],
)
async def get_many_by_building(
    building_id: int,
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByBuildingQuery(building_id=building_id, pagination=pagination)
    use_case = GetManyByBuildingUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get(
    "/organizations/by-activity/{activity_id}",
    response_model=WithPaginationResponse[ResponseOrganization],
)
async def get_many_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityQuery(activity_id=activity_id, pagination=pagination)
    use_case = GetManyByActivityUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get(
    "/organizations/by-geolocation",
    response_model=WithTotalCountResponse[ResponseOrganization],
)
async def get_many_by_geo(
    db: AsyncSession = Depends(get_read_db),
    location: FilterByLocation = Depends(),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByGeoQuery(location=location)
    use_case = GetManyByGeoUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get(
    "/organizations/by-activity-tree/{activity_id}",
    response_model=WithPaginationResponse[ResponseOrganization],
)
async def get_many_by_activity_tree(
    activity_id: int,
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByActivityTreeQuery(activity_id=activity_id, pagination=pagination)
    use_case = GetManyByActivityTreeUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get(
    "/organizations/search",
    response_model=WithPaginationResponse[ResponseOrganization],
)
async def get_many_by_name(
    db: AsyncSession = Depends(get_read_db),
    pagination: Pagination = Depends(),
    filters: FilterByName = Depends(),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetManyByNameQuery(pagination=pagination, filters=filters)
    use_case = GetManyByNameUseCase(
        organization_repository=organization_query_repository
    )
    return await use_case.execute(query)


@router.get("/organizations/{organization_id}", response_model=OrganizationDetail)
async def get_one_by_id(
    organization_id: int,
    db: AsyncSession = Depends(get_read_db),
    _api_key=Depends(verify_api_key),
):
    organization_query_repository = OrganizationQueryRepository(db)
    query = GetOneByIdQuery(organization_id=organization_id)
    use_case = GetOneByIdUseCase(organization_repository=organization_query_repository)
    return await use_case.execute(query)
