from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.common import Pagination, Filters


class OrganizationQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def getManyByBuilding(
        self, building_id: int, pagination: Pagination
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit
        total_count = await self.session.scalar(
            text('SELECT COUNT(*) FROM "organization" WHERE build_id = :building_id'),
            {"building_id": building_id},
        )
        organizations_query = text(
            """
                WITH paginated_organizations AS (
                    SELECT id, name
                    FROM "organization"
                    WHERE build_id = :building_id
                    LIMIT :limit OFFSET :offset
                )
                SELECT
                    "paginated_organizations".id AS organization_id,
                    "paginated_organizations".name AS organization_name
                FROM "paginated_organizations"
            """
        )
        rows = await self.session.execute(
            organizations_query,
            {"building_id": building_id, "offset": offset, "limit": pagination.limit},
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organizations": []}
            organization_map = {}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if organization_id not in organization_map:
                    organization_obj = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                    }
                    organization_map[organization_id] = organization_obj
                    result["organizations"].append(organization_obj)
                else:
                    organization_obj = organization_map[organization_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return {
            "data": value,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def getManyByActivity(
        self, activity_id: int, pagination: Pagination
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit
        total_count = await self.session.scalar(
            text(
                """
                    SELECT COUNT(*)
                    FROM organization
                    JOIN organization_activity ON organization.id = organization_activity.organization_id
                    WHERE organization_activity.activity_id = :activity_id
                """
            ),
            {"activity_id": activity_id},
        )
        organizations_query = text(
            """
                WITH paginated_organizations AS (
                    SELECT o.id, o.name
                    FROM organization o
                    JOIN organization_activity oa ON o.id = oa.organization_id
                    WHERE oa.activity_id = :activity_id
                    LIMIT :limit OFFSET :offset
                )
                SELECT
                    paginated_organizations.id AS organization_id,
                    paginated_organizations.name AS organization_name
                FROM paginated_organizations
            """
        )

        rows = await self.session.execute(
            organizations_query,
            {
                "activity_id": activity_id,
                "offset": offset,
                "limit": pagination.limit,
            },
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organizations": []}
            organization_map = {}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if organization_id not in organization_map:
                    organization_obj = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                    }
                    organization_map[organization_id] = organization_obj
                    result["organizations"].append(organization_obj)
                else:
                    organization_obj = organization_map[organization_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return {
            "data": value,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def getManyByGeo(self) -> list[dict]:
        organizations_query = text(
            """
                SELECT
                    "organization".id AS organization_id,
                    "organization".name AS organization_name
                FROM "organization"
            """
        )
        rows = await self.session.execute(
            organizations_query,
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organizations": []}
            organization_map = {}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if organization_id not in organization_map:
                    organization_obj = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                    }
                    organization_map[organization_id] = organization_obj
                    result["organizations"].append(organization_obj)
                else:
                    organization_obj = organization_map[organization_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return value

    async def getOneById(self, organization_id: int) -> dict:
        organization_query = text(
            """
                SELECT
                    "organization".id AS organization_id,
                    "organization".name AS organization_name,
                    "telephone".id AS telephone_id,
                    "telephone".phone_number AS telephone_phone_number,
                    "activity".id AS activity_id,
                    "activity".name AS activity_name,
                    "build".id AS build_id,
                    "build".address AS build_address,
                    ST_Y("build".location::geometry) AS build_latitude,
                    ST_X("build".location::geometry) AS build_longitude
                FROM "organization"
                LEFT JOIN "telephone" ON "telephone".organization_id = "organization".id
                LEFT JOIN "organization_activity" oa ON oa.organization_id = "organization".id
                LEFT JOIN "activity" ON "activity".id = oa.activity_id
                LEFT JOIN "build" ON "build".id = "organization".build_id
                WHERE "organization".id = :organization_id
            """
        )
        rows = await self.session.execute(
            organization_query, {"organization_id": organization_id}
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organization": None}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if result["organization"] is None:
                    result["organization"] = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                        "telephones": [],
                        "activities": [],
                        "build": (
                            {
                                "address": row[column_headers.index("build_address")],
                                "latitude": row[column_headers.index("build_latitude")],
                                "longitude": row[
                                    column_headers.index("build_longitude")
                                ],
                            }
                            if row[column_headers.index("build_id")] is not None
                            else None
                        ),
                    }
                    organization_obj = result["organization"]
                telephone_id = row[column_headers.index("telephone_id")]
                if telephone_id is not None:
                    telephone_map = {d["id"]: d for d in organization_obj["telephones"]}
                    if telephone_id not in telephone_map:
                        telephone_obj = {
                            "id": telephone_id,
                            "phone_number": row[
                                column_headers.index("telephone_phone_number")
                            ],
                        }
                        organization_obj["telephones"].append(telephone_obj)
                activity_id = row[column_headers.index("activity_id")]
                if activity_id is not None:
                    activity_map = {d["id"]: d for d in organization_obj["activities"]}
                    if activity_id not in activity_map:
                        activity_obj = {
                            "id": activity_id,
                            "name": row[column_headers.index("activity_name")],
                        }
                        organization_obj["activities"].append(activity_obj)
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return value

    async def getManyByActivityAll(self, pagination: Pagination) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit
        total_count = await self.session.scalar(
            text('SELECT COUNT(*) FROM "organization"')
        )
        organizations_query = text(
            """
                WITH paginated_organizations AS (
                    SELECT id, name
                    FROM "organization"
                    LIMIT :limit OFFSET :offset
                )
                SELECT
                    "paginated_organizations".id AS organization_id,
                    "paginated_organizations".name AS organization_name
                FROM "paginated_organizations"
            """
        )
        rows = await self.session.execute(
            organizations_query, {"offset": offset, "limit": pagination.limit}
        )
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organizations": []}
            organization_map = {}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if organization_id not in organization_map:
                    organization_obj = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                    }
                    organization_map[organization_id] = organization_obj
                    result["organizations"].append(organization_obj)
                else:
                    organization_obj = organization_map[organization_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return {
            "data": value,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def getByName(self, pagination: Pagination, filters: Filters) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit
        where_clause = ""
        params = {"offset": offset, "limit": pagination.limit}
        if filters.name:
            where_clause = "WHERE name ILIKE :name"
            params["name"] = f"%{filters.name}%"

        total_count = await self.session.scalar(
            text(f'SELECT COUNT(*) FROM "organization" {where_clause}'), params
        )
        organizations_query = text(
            f"""
                WITH paginated_organizations AS (
                    SELECT id, name
                    FROM "organization"
                    {where_clause}
                    LIMIT :limit OFFSET :offset
                )
                SELECT
                    "paginated_organizations".id AS organization_id,
                    "paginated_organizations".name AS organization_name
                FROM "paginated_organizations"
            """
        )
        rows = await self.session.execute(organizations_query, params)
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"organizations": []}
            organization_map = {}
            for row in data:
                organization_id = row[column_headers.index("organization_id")]
                if organization_id not in organization_map:
                    organization_obj = {
                        "id": organization_id,
                        "name": row[column_headers.index("organization_name")],
                    }
                    organization_map[organization_id] = organization_obj
                    result["organizations"].append(organization_obj)
                else:
                    organization_obj = organization_map[organization_id]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return {
            "data": value,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }
