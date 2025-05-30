from ...repositories import OrganizationQueryRepository
from src.common import Pagination


class GetManyByBuildingQuery:
    def __init__(self, building_id: int, pagination: Pagination):
        self.building_id = building_id
        self.pagination = pagination


class GetManyByBuildingUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByBuildingQuery):
        organization = await self.organization_repository.get_many_by_building(
            query.building_id, query.pagination
        )
        return organization
