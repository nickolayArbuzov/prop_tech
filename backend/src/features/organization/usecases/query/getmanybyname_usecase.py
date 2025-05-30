from ...repositories import OrganizationQueryRepository
from src.common import Pagination, FilterByName


class GetManyByNameQuery:
    def __init__(self, pagination: Pagination, filters: FilterByName):
        self.pagination = pagination
        self.filters = filters


class GetManyByNameUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByNameQuery):
        organization = await self.organization_repository.get_many_by_name(
            query.pagination, query.filters
        )
        return organization
