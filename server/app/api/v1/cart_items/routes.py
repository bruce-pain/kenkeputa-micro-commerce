from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.v1.cart_items import schemas
from app.api.services.cart_item import CartItemService
from app.api.models.user import User
from app.db.database import get_db
from app.core.dependencies.security import get_current_user

cart = APIRouter(prefix="/cart", tags=["Cart"])


@cart.post(
    path="",
    response_model=schemas.CartItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add item to cart",
    description="Add a product to the user's cart. If the product already exists in the cart, the quantity will be incremented.",
)
def add_item_to_cart(
    schema: schemas.CartItemCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = CartItemService(db)
    return schemas.CartItemResponse(
        status_code=status.HTTP_201_CREATED,
        message="Item added to cart successfully",
        data=service.add_item_to_cart(current_user, schema),
    )


@cart.get(
    path="",
    response_model=schemas.CartItemListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user cart",
    description="Retrieve all items in the user's cart with product details and total cart value.",
)
def get_user_cart(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = CartItemService(db)
    return schemas.CartItemListResponse(
        status_code=status.HTTP_200_OK,
        message="Cart retrieved successfully",
        data=service.get_user_cart(current_user),
    )


@cart.put(
    path="/{item_id}",
    response_model=schemas.CartItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update cart item quantity",
    description="Update the quantity of a specific cart item. Validates stock availability.",
)
def update_cart_item(
    item_id: str,
    schema: schemas.CartItemUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = CartItemService(db)
    return schemas.CartItemResponse(
        status_code=status.HTTP_200_OK,
        message="Cart item updated successfully",
        data=service.update_cart_item(item_id, current_user, schema),
    )


@cart.delete(
    path="/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove item from cart",
    description="Remove a specific item from the user's cart.",
)
def remove_cart_item(
    item_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = CartItemService(db)
    service.remove_cart_item(item_id, current_user)


@cart.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear cart",
    description="Remove all items from the user's cart.",
)
def clear_user_cart(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = CartItemService(db)
    service.clear_user_cart(current_user)
