from ...repositories import OrganizationQueryRepository
from src.common.pagination import Pagination

class GetManyByBuildingQuery:
    def __init__(self, pagination: Pagination):
        self.pagination = pagination

class GetManyByBuildingUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByBuildingQuery):
        organization = await self.organization_repository.getManyByBuilding(query.pagination)
        return organization
