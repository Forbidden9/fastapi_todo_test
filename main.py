from fastapi import FastAPI

from api import router as api_router
from core import router as oauth_router
from core.database.session import Base, engine
from core.settings.settings import settings

app = FastAPI(
    title = str(settings.PROJECT_NAME),
    version = str(settings.PROJECT_VERSION),
    swagger_ui_parameters = {"docExpansion": "none"}
)

app.include_router(api_router)
app.include_router(oauth_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return "Welcome, Thanks for use this project - Backend Developer Test"