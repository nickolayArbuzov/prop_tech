from ...repositories import OrganizationQueryRepository
from src.common import Pagination, FilterByName


class GetByNameQuery:
    def __init__(self, pagination: Pagination, filters: FilterByName):
        self.pagination = pagination
        self.filters = filters


class GetByNameUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetByNameQuery):
        organization = await self.organization_repository.getByName(
            query.pagination, query.filters
        )
        return organization
