from ...repositories import BuildQueryRepository
from src.common import Pagination


class GetManyQuery:
    def __init__(self, pagination: Pagination):
        self.pagination = pagination


class GetManyUseCase:
    def __init__(self, build_repository: BuildQueryRepository):
        self.build_repository = build_repository

    async def execute(self, query: GetManyQuery):
        build = await self.build_repository.get_many(query.pagination)
        return build
