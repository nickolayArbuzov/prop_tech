from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, cast
from geoalchemy2.types import Geometry
from geoalchemy2.functions import ST_X, ST_Y
from src.features.build.build_model import Build
from src.common import Pagination


class BuildQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_many(self, pagination: Pagination) -> dict:
        offset = (pagination.page - 1) * pagination.limit

        total_count = await self.session.scalar(select(func.count()).select_from(Build))

        result = (
            await self.session.execute(
                select(
                    Build.id.label("id"),
                    Build.address.label("address"),
                    ST_Y(cast(Build.location, Geometry)).label("latitude"),
                    ST_X(cast(Build.location, Geometry)).label("longitude"),
                )
                .limit(pagination.limit)
                .offset(offset)
            )
        ).all()

        return {
            "data": result,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }
