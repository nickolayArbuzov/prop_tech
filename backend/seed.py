import asyncio
import random
from datetime import datetime
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from src.database import async_session
from src.features.build.build_model import Build
from src.features.organization.organization_model import Organization
from src.features.telephone.telephone_model import Telephone
from src.features.activity.activity_model import Activity
from src.features.organization.organization_model import organization_activity


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
    "Интеллект-Софт",
    "СканЭнерго",
    "Архитектура Про",
    "УК Городская Среда",
]


ACTIVITY_TREE = [
    ("Информационные технологии", None),
    ("Разработка ПО", "Информационные технологии"),
    ("Веб-разработка", "Разработка ПО"),
    ("Мобильная разработка", "Разработка ПО"),
    ("Системное программирование", "Разработка ПО"),
    ("Строительство", None),
    ("Жилищное строительство", "Строительство"),
    ("Капитальный ремонт", "Жилищное строительство"),
    ("Фасадные работы", "Жилищное строительство"),
    ("Инженерные сети", "Жилищное строительство"),
    ("Здравоохранение", None),
    ("Стоматология", "Здравоохранение"),
    ("Терапевтическая стоматология", "Стоматология"),
    ("Хирургическая стоматология", "Стоматология"),
    ("Ортодонтия", "Стоматология"),
    ("Промышленное производство", None),
    ("Пищевая промышленность", "Промышленное производство"),
    ("Производство хлебобулочных изделий", "Пищевая промышленность"),
    ("Производство молочной продукции", "Пищевая промышленность"),
    ("Производство мясных изделий", "Пищевая промышленность"),
    ("Металлообработка", "Промышленное производство"),
    ("Машиностроение", "Промышленное производство"),
]


async def seed():
    async with async_session() as session:
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

            name_to_activity = {}
            for name, parent_name in ACTIVITY_TREE:
                activity = Activity(
                    name=name,
                    parent=name_to_activity.get(parent_name),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(activity)
                name_to_activity[name] = activity

            organizations = []
            org_names = ORGANIZATION_NAMES[:20]
            for name in org_names:
                org = Organization(
                    name=name,
                    build=random.choice(builds),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(org)
                organizations.append(org)

            for org in organizations:
                for _ in range(random.randint(1, 3)):
                    phone = Telephone(
                        phone_number=f"+7-495-{random.randint(1000000, 9999999)}",
                        organization=org,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    session.add(phone)

            leaf_activities = [a for a in name_to_activity.values() if not a.children]
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
