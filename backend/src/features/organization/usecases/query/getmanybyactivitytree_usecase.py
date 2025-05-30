from ...repositories import OrganizationQueryRepository
from src.common import Pagination


class GetManyByActivityTreeQuery:
    def __init__(self, activity_id: int, pagination: Pagination):
        self.activity_id = activity_id
        self.pagination = pagination


class GetManyByActivityTreeUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByActivityTreeQuery):
        organization = await self.organization_repository.getManyByActivityTree(
            query.activity_id, query.pagination
        )
        return organization
