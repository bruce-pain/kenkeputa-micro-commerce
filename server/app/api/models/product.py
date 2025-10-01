"""Product data model"""

from sqlalchemy import Column, String, DECIMAL, INTEGER
from app.core.base.model import BaseTableModel


class Product(BaseTableModel):
    __tablename__ = "products"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # 2 decimal places
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(INTEGER, nullable=False, default=0)

    def __str__(self):
        return "Product: {}\nDescription: {}\nPrice: {}\nStock: {}".format(self.name, self.description, self.price, self.stock)