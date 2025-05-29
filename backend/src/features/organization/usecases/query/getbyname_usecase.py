from ...repositories import OrganizationQueryRepository

class GetByNameQuery:
    def __init__(self):
        pass

class GetByNameUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetByNameQuery):
        organization = await self.organization_repository.getByName()
        return organization
