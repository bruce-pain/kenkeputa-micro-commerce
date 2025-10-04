"""CartItem data model"""

from sqlalchemy import Column, String, Integer, ForeignKey
from app.core.base.model import BaseTableModel
from sqlalchemy.orm import relationship

class CartItem(BaseTableModel):
    __tablename__ = "cart_items"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return "CartItem: User ID: {}, Product ID: {}, Quantity: {}".format(self.user_id, self.product_id, self.quantity)