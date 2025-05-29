from ...repositories import OrganizationQueryRepository

class GetManyByGeoQuery:
    def __init__(self):
        pass

class GetManyByGeoUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetManyByGeoQuery):
        organization = await self.organization_repository.getManyByGeo()
        return organization
