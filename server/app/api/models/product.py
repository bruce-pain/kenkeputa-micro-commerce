"""Product data model"""

from sqlalchemy import Column, String, DECIMAL, Integer
from app.core.base.model import BaseTableModel
from sqlalchemy.orm import relationship


class Product(BaseTableModel):
    __tablename__ = "products"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # 2 decimal places
    price = Column(DECIMAL(10, 2), nullable=False)

    stock = Column(Integer, nullable=False, default=0)

    # relationships
    cart_items = relationship("CartItem", back_populates="product")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return "Product: {}\nDescription: {}\nPrice: {}\nStock: {}".format(self.name, self.description, self.price, self.stock)