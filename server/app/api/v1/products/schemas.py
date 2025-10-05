from typing import Annotated, Optional
from decimal import Decimal

from pydantic import BaseModel, StringConstraints
from app.core.base.schema import BaseResponseModel, PaginatedResponseModel


class ProductBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=255)]
    description: Optional[str] = None
    price: Decimal
    stock: int = 0


class ProductCreateRequest(ProductBase):
    pass


class ProductUpdateRequest(BaseModel):
    name: Optional[Annotated[str, StringConstraints(max_length=255)]] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None


class ProductResponseData(ProductBase):
    id: str


class ProductResponse(BaseResponseModel):
    data: ProductResponseData


class ProductListResponse(PaginatedResponseModel):
    pass
