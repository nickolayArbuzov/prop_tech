from ...repositories import OrganizationQueryRepository
from src.common import Pagination


class GetManyByActivityQuery:
    def __init__(self, activity_id: int, pagination: Pagination):
        self.activity_id = activity_id
        self.pagination = pagination


class GetManyByActivityUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByActivityQuery):
        organization = await self.organization_repository.get_many_by_activity(
            query.activity_id, query.pagination
        )
        return organization
