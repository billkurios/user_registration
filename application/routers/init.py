from fastapi import APIRouter

from .user_router import user_router

router = APIRouter(
    prefix="/api",
    tags=["api", "latest"],
)

router.include_router(user_router)