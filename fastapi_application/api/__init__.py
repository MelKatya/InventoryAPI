from fastapi import APIRouter

from .users import router as users_route

router = APIRouter()

router.include_router(users_route, prefix="/users")
