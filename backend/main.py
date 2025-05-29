from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.features.organization import organization_controller
from src.features.organization import organization_model
from src.features.telephone import telephone_controller
from src.features.telephone import telephone_model
from src.features.build import build_controller
from src.features.build import build_model
from src.features.activity import activity_controller
from src.features.activity import activity_model

async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(organization_controller.router, prefix='/api', tags=['organization'])
app.include_router(telephone_controller.router, prefix='/api', tags=['telephone'])
app.include_router(build_controller.router, prefix='/api', tags=['build'])
app.include_router(activity_controller.router, prefix='/api', tags=['activity'])


