from fastapi import APIRouter
from core.oauth.router import oauth


router = APIRouter()

router.include_router(oauth, tags=["oauth"], prefix="/api/oauth")
