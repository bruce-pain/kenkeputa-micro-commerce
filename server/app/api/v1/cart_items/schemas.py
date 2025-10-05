from pydantic import BaseModel, Field

from app.core.base.schema import BaseResponseModel


class CartProduct(BaseModel):
    id: str
    name: str
    unit_price: float
    stock: int  # Added stock to show availability


class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")


class CartItemResponse(BaseResponseModel):
    id: str 
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    product: CartProduct
    created_at: str


# create
class CartItemCreateRequest(CartItemBase):
    pass


# update
class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")


# list
class CartItemListResponse(BaseResponseModel):
    total_cart_value: float
    items_count: int  # Added count for convenience
    data: list[CartItemResponse]