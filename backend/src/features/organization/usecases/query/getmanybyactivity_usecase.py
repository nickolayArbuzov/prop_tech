from ...repositories import OrganizationQueryRepository
from src.common.pagination import Pagination

class GetManyByActivityQuery:
    def __init__(self, pagination: Pagination):
        self.pagination = pagination

class GetManyByActivityUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByActivityQuery):
        organization = await self.organization_repository.getManyByActivity(query.pagination)
        return organization
