from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.features.organization import organization_controller
from src.features.build import build_controller


async def lifespan(app):
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(organization_controller.router, prefix="/api", tags=["organization"])
app.include_router(build_controller.router, prefix="/api", tags=["build"])
