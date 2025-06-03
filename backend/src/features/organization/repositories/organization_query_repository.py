from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import cast, text, select, func
from sqlalchemy.orm import aliased, selectinload
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint, ST_DWithin
from geoalchemy2 import Geography
from geoalchemy2.types import Geometry
from geoalchemy2.functions import ST_X, ST_Y
from src.common import Pagination, FilterByName, FilterByLocation
from src.features.organization.organization_model import (
    Organization,
    organization_activity,
)
from src.features.build.build_model import Build
from src.features.activity.activity_model import Activity


class OrganizationQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_many_by_building(
        self, building_id: int, pagination: Pagination
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit

        total_count = await self.session.scalar(
            select(func.count()).select_from(
                select(Organization.id)
                .where(Organization.build_id == building_id)
                .subquery()
            )
        )

        result = (
            await self.session.execute(
                (
                    select(Organization.id.label("id"), Organization.name.label("name"))
                    .where(Organization.build_id == building_id)
                    .limit(pagination.limit)
                    .offset(offset)
                )
            )
        ).all()

        return {
            "data": result,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def get_many_by_activity(
        self, activity_id: int, pagination: Pagination
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit

        total_count_stmt = (
            select(func.count())
            .select_from(organization_activity)
            .where(organization_activity.c.activity_id == activity_id)
        )
        total_count = await self.session.scalar(total_count_stmt)

        org_alias = aliased(Organization)

        result = (
            await self.session.execute(
                (
                    select(org_alias.id.label("id"), org_alias.name.label("name"))
                    .join(
                        organization_activity,
                        org_alias.id == organization_activity.c.organization_id,
                    )
                    .where(organization_activity.c.activity_id == activity_id)
                    .limit(pagination.limit)
                    .offset(offset)
                )
            )
        ).all()

        return {
            "data": result,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def get_many_by_geo(self, location: FilterByLocation) -> list[dict]:
        if not (location.latitude and location.longitude and location.radius):
            return {
                "data": [],
                "total": 0,
            }

        point = ST_SetSRID(ST_MakePoint(location.longitude, location.latitude), 4326)

        total_count_stmt = (
            select(func.count())
            .select_from(Organization)
            .join(Build, Build.id == Organization.build_id)
            .where(ST_DWithin(Build.location, point.cast(Geography), location.radius))
        )
        total_count = await self.session.scalar(total_count_stmt)

        result = (
            await self.session.execute(
                (
                    select(Organization.id.label("id"), Organization.name.label("name"))
                    .join(Build, Build.id == Organization.build_id)
                    .where(
                        ST_DWithin(
                            Build.location, point.cast(Geography), location.radius
                        )
                    )
                )
            )
        ).all()

        return {
            "data": result,
            "total": total_count,
        }

    async def get_one_by_id(self, organization_id: int) -> dict:

        result = await self.session.execute(
            select(Organization)
            .options(
                selectinload(Organization.telephones),
                selectinload(Organization.activities),
                selectinload(Organization.build),
            )
            .where(Organization.id == organization_id)
        )
        organization = result.scalar_one_or_none()

        if not organization:
            return None

        build = organization.build
        if build and build.location:
            build.latitude = await self.session.scalar(
                select(ST_Y(cast(build.location, Geometry))).where(Build.id == build.id)
            )
            build.longitude = await self.session.scalar(
                select(ST_X(cast(build.location, Geometry))).where(Build.id == build.id)
            )

        return organization

    async def get_many_by_activity_tree(
        self, activity_id: int, pagination: Pagination
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit

        activity_tree = (
            select(Activity.id)
            .where(Activity.id == activity_id)
            .cte(name="activity_tree", recursive=True)
        )

        a = aliased(Activity)
        activity_tree = activity_tree.union_all(
            select(a.id).where(a.parent_id == activity_tree.c.id)
        )

        total_count_stmt = (
            select(func.count(func.distinct(Organization.id)))
            .join(
                organization_activity,
                Organization.id == organization_activity.c.organization_id,
            )
            .where(organization_activity.c.activity_id.in_(select(activity_tree.c.id)))
        )
        total_count = await self.session.scalar(total_count_stmt)

        org_query = (
            select(Organization)
            .join(
                organization_activity,
                Organization.id == organization_activity.c.organization_id,
            )
            .where(organization_activity.c.activity_id.in_(select(activity_tree.c.id)))
            .distinct()
            .offset(offset)
            .limit(pagination.limit)
        )

        result = (await self.session.execute(org_query)).scalars().all()

        return {
            "data": [{"id": org.id, "name": org.name} for org in result],
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }

    async def get_many_by_name(
        self, pagination: Pagination, filters: FilterByName
    ) -> list[dict]:
        offset = (pagination.page - 1) * pagination.limit

        query = select(Organization)

        if filters.name:
            query = query.where(Organization.name.ilike(f"%{filters.name}%"))

        count_query = (
            select(func.count())
            .select_from(Organization)
            .where(Organization.name.ilike(f"%{filters.name}%"))
            if filters.name
            else select(func.count()).select_from(Organization)
        )
        total_count = await self.session.scalar(count_query)

        result = (
            (await self.session.execute(query.offset(offset).limit(pagination.limit)))
            .scalars()
            .all()
        )

        return {
            "data": result,
            "total": total_count,
            "page": pagination.page,
            "limit": pagination.limit,
        }
