from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, StringConstraints
from app.core.base.schema import BaseResponseModel, PaginatedResponseModel


class ProductBase(BaseModel):
    name: Annotated[str, StringConstraints(max_length=255)]
    description: str | None = None 
    price: Decimal
    stock: int = 0 


class ProductCreateRequest(ProductBase):
    pass


class ProductUpdateRequest(BaseModel):
    name: Annotated[str, StringConstraints(max_length=255)] | None = None
    description: str | None = None
    price: Decimal | None = None
    stock: int | None = None


class ProductResponseData(ProductBase):
    id: str


class ProductResponse(BaseResponseModel):
    data: ProductResponseData


class ProductListResponse(PaginatedResponseModel):
    pass