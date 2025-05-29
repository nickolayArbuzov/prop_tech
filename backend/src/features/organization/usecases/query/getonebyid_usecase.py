from fastapi import HTTPException
from ...repositories import OrganizationQueryRepository

class GetOneByIdQuery:
    def __init__(self, organization_id: int):
        self.organization_id = organization_id

class GetOneByIdUseCase:
    def __init__(self, organization_repository: OrganizationQueryRepository):
        self.organization_repository = organization_repository

    async def execute(self, query: GetOneByIdQuery):
        organization = await self.organization_repository.getOneById(query.organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        return organization
