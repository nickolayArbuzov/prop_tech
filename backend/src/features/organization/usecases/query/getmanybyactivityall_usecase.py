from ...repositories import OrganizationQueryRepository
from src.common.pagination import Pagination

class GetManyByActivityAllQuery:
    def __init__(self, pagination: Pagination):
        self.pagination = pagination

class GetManyByActivityAllUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByActivityAllQuery):
        organization = await self.organization_repository.getManyByActivityAll(query.pagination)
        return organization
