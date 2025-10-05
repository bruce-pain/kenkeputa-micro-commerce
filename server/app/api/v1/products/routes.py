from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.models.product import Product
from app.api.models.user import User
from app.api.services.product import ProductService
from app.api.v1.products import schemas
from app.core.dependencies.security import get_current_admin_user, get_current_user
from app.db.database import get_db

products = APIRouter(prefix="/products")

@products.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProductListResponse,
    summary="Get list of products with filters",
    description="Retrieve a list of products with optional filters such as name, price range, and availability.",
    tags=["Products"],
)
def list_products(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    available: bool | None = None,
    page: int = 1,
    limit: int = 10,
):
    service = ProductService(db=db)
    result = service.list_products(
        name=q,
        in_stock=available,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=limit,
    )
    result.items = [schemas.ProductResponseData(**item.to_dict()) for item in result.items]
    return schemas.ProductListResponse(
        status_code=status.HTTP_200_OK,
        message="Products retrieved successfully",
        data=result,
    )


@products.post(
    path="",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new product",
    description="This endpoint creates a new product.",
    tags=["Admin"],
)
def create_product(
    schema: schemas.ProductCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    service = ProductService(db=db)
    product = service.create_product(schema=schema)
    return schemas.ProductResponse(
        status_code=status.HTTP_201_CREATED,
        message="Product created successfully",
        data=schemas.ProductResponseData(**product.to_dict()),
    )


@products.get(
    path="/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get single product by ID",
    description="Retrieve a single product by its unique ID.",
    tags=["Products"],
)
def retrieve_product(
    product_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = ProductService(db=db)
    product = service.retrieve_product(product_id=product_id)
    return schemas.ProductResponse(
        status_code=status.HTTP_200_OK,
        message="Product retrieved successfully",
        data=schemas.ProductResponseData(**product.to_dict()),
    )


@products.put(
    path="/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update product",
    description="Update an existing product by its ID.",
    tags=["Admin"],
)
def update_product(
    product_id: str,
    schema: schemas.ProductUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    service = ProductService(db=db)
    product = service.update_product(product_id=product_id, schema=schema)
    return schemas.ProductResponse(
        status_code=status.HTTP_200_OK,
        message="Product updated successfully",
        data=schemas.ProductResponseData(**product.to_dict()),
    )


@products.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product by its ID.",
    tags=["Admin"],
)
def delete_product(
    product_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    service = ProductService(db=db)
    service.delete_product(product_id=product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
