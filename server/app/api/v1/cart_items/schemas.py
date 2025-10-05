from pydantic import BaseModel
from typing import Optional

from app.core.base.schema import BaseResponseModel


class CartProduct(BaseModel):
    id: str
    name: str
    unit_price: float

class CartItemBase(BaseModel):
    product_id: str
    quantity: int

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
    quantity: Optional[int] = None

# list
class CartItemListResponse(BaseResponseModel):
    total_cart_value: float
    data: list[CartItemResponse]