import asyncio
import random
from datetime import datetime
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from src.database import AsyncSessionLocal
from src.features.build.build_model import Build
from src.features.organization.organization_model import (
    Organization,
    organization_activity,
)
from src.features.telephone.telephone_model import Telephone
from src.features.activity.activity_model import Activity

ADDRESSES_WITH_COORDS = [
    ("Москва, ул. Арбат, д. 12", (55.752023, 37.586397)),
    ("Москва, Ленинградский пр-т, д. 37к1", (55.790818, 37.541073)),
    ("Москва, ул. Тверская, д. 7", (55.758206, 37.615677)),
    ("Москва, пр-т Мира, д. 119", (55.821509, 37.639440)),
    ("Москва, ул. Новый Арбат, д. 21", (55.751685, 37.588496)),
    ("Москва, ул. Мясницкая, д. 13", (55.763008, 37.635726)),
    ("Москва, ул. Сретенка, д. 28", (55.768413, 37.633752)),
    ("Москва, ул. Профсоюзная, д. 90", (55.645090, 37.547710)),
    ("Москва, ул. Бауманская, д. 20", (55.772487, 37.678459)),
    ("Москва, ул. Краснопролетарская, д. 16", (55.777675, 37.598607)),
]

ORGANIZATION_NAMES = [
    "Техносфера",
    "Инжстройпроект",
    "Медика Групп",
    "АльфаСтройИнвест",
    "ПромТехСервис",
    "Городская Клиника №12",
    "КодПроект",
    "ДомИнвест",
    "СтройМонтажСервис",
    "Инновации 24",
    "Стоматология Улыбка",
    "ИТ Коннект",
    "Здоровье Плюс",
    "Омега Девелопмент",
    "Дента-Проф",
    "АйТи-Решения",
    "Городская поликлиника №75",
    "ПромИнжСервис",
    "Сити-Дент",
    "Бизнес Решения",
]

ACTIVITY_TREE = [
    {"id": 1, "name": "Информационные технологии", "parent_id": None},
    {"id": 2, "name": "Разработка ПО", "parent_id": 1},
    {"id": 3, "name": "Веб-разработка", "parent_id": 2},
    {"id": 4, "name": "Мобильная разработка", "parent_id": 2},
    {"id": 5, "name": "Системное программирование", "parent_id": 2},
    {"id": 6, "name": "Строительство", "parent_id": None},
    {"id": 7, "name": "Жилищное строительство", "parent_id": 6},
    {"id": 8, "name": "Капитальный ремонт", "parent_id": 7},
    {"id": 9, "name": "Фасадные работы", "parent_id": 7},
    {"id": 10, "name": "Инженерные сети", "parent_id": 7},
    {"id": 11, "name": "Здравоохранение", "parent_id": None},
    {"id": 12, "name": "Стоматология", "parent_id": 11},
    {"id": 13, "name": "Терапевтическая стоматология", "parent_id": 12},
    {"id": 14, "name": "Хирургическая стоматология", "parent_id": 12},
    {"id": 15, "name": "Ортодонтия", "parent_id": 12},
    {"id": 16, "name": "Промышленное производство", "parent_id": None},
    {"id": 17, "name": "Пищевая промышленность", "parent_id": 16},
    {"id": 18, "name": "Производство хлебобулочных изделий", "parent_id": 17},
    {"id": 19, "name": "Производство молочной продукции", "parent_id": 17},
    {"id": 20, "name": "Производство мясных изделий", "parent_id": 17},
    {"id": 21, "name": "Металлообработка", "parent_id": 16},
    {"id": 22, "name": "Машиностроение", "parent_id": 16},
]


async def seed():
    async with AsyncSessionLocal() as session:
        async with session.begin():

            builds = []
            for address, (lat, lon) in ADDRESSES_WITH_COORDS:
                b = Build(
                    address=address,
                    location=from_shape(Point(lon, lat), srid=4326),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(b)
                builds.append(b)

            activities_by_id = {}
            for activity_data in ACTIVITY_TREE:
                activity = Activity(
                    id=activity_data["id"],
                    name=activity_data["name"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                activities_by_id[activity_data["id"]] = activity

            for activity_data in ACTIVITY_TREE:
                parent_id = activity_data["parent_id"]
                if parent_id:
                    activities_by_id[activity_data["id"]].parent = activities_by_id[
                        parent_id
                    ]

            session.add_all(activities_by_id.values())

            organizations = []
            for name in ORGANIZATION_NAMES[:20]:
                org = Organization(
                    name=name,
                    build=random.choice(builds),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(org)
                organizations.append(org)

            await session.flush()

            for org in organizations:
                for _ in range(random.randint(1, 3)):
                    phone = Telephone(
                        phone_number=f"+7-495-{random.randint(1000000, 9999999)}",
                        organization=org,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    session.add(phone)

            used_as_parent_ids = {
                activity["parent_id"]
                for activity in ACTIVITY_TREE
                if activity["parent_id"] is not None
            }

            leaf_activities = [
                act
                for act_id, act in activities_by_id.items()
                if act_id not in used_as_parent_ids
            ]

            for org in organizations:
                chosen = random.sample(leaf_activities, k=random.randint(1, 3))
                for act in chosen:
                    await session.execute(
                        organization_activity.insert().values(
                            organization_id=org.id, activity_id=act.id
                        )
                    )


if __name__ == "__main__":
    asyncio.run(seed())
