from fastapi import APIRouter

from app.api.v1.auth.routes import auth
from app.api.v1.products.routes import products
from app.api.v1.cart_items.routes import cart

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(router=auth)
main_router.include_router(router=products)
main_router.include_router(router=cart)
