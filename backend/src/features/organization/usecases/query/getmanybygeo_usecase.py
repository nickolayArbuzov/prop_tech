from ...repositories import OrganizationQueryRepository
from src.common import FilterByLocation


class GetManyByGeoQuery:
    def __init__(self, location: FilterByLocation):
        self.location = location


class GetManyByGeoUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByGeoQuery):
        organization = await self.organization_repository.get_many_by_geo(
            query.location
        )
        return organization
