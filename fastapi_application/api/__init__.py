from fastapi import APIRouter

from .users import router as users_route
from .authentication import router as auth_route

router = APIRouter()

router.include_router(users_route, prefix="/users")
router.include_router(auth_route, prefix="/auth")
