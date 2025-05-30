from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.common import Pagination


class BuildQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getMany(self, pagination: Pagination) -> dict:
        offset = (pagination.page - 1) * pagination.limit
        total_count = await self.session.scalar(text('SELECT COUNT(*) FROM "build"'))
        builds_query = text(
            """
                WITH paginated_builds AS (
                    SELECT id, address, ST_Y(location::geometry) AS latitude, ST_X(location::geometry) AS longitude
                    FROM "build"
                    LIMIT :limit OFFSET :offset
                )
                SELECT
                    "paginated_builds".id AS build_id,
                    "paginated_builds".address AS build_address,
                    "paginated_builds".latitude AS build_latitude,
                    "paginated_builds".longitude AS build_longitude
                FROM "paginated_builds"
            """
        )
        rows = await self.session.execute(
            builds_query, {"offset": offset, "limit": pagination.limit}
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"builds": []}
            build_map = {}
            for row in data:
                build_id = row[column_headers.index("build_id")]
                if build_id not in build_map:
                    build_obj = {
                        "id": build_id,
                        "address": row[column_headers.index("build_address")],
                        "latitude": row[column_headers.index("build_latitude")],
                        "longitude": row[column_headers.index("build_longitude")],
                    }
                    build_map[build_id] = build_obj
                    result["builds"].append(build_obj)
                else:
                    build_obj = build_map[build_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return {
            "data": value,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }
