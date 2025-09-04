from fastapi import APIRouter
from api.task.router import task


router = APIRouter()

router.include_router(task, tags=["task"], prefix="/api")
