from fastapi import APIRouter

from .users import router as users_route
from .authentication import router as auth_route
from .products import router as product_route
from .orders import router as order_route

router = APIRouter()

router.include_router(users_route, prefix="/users")
router.include_router(auth_route, prefix="/auth")
router.include_router(product_route, prefix="/products")
router.include_router(order_route, prefix="/orders")
