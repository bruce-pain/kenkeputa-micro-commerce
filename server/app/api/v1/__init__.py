from fastapi import APIRouter

from app.api.v1.auth.routes import auth
from app.api.v1.products.routes import products

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(router=auth)
main_router.include_router(router=products)
