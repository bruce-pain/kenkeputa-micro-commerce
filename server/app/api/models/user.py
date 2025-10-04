"""User data model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.base.model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)

    # add role column as a string
    # possible values: 'admin', 'user'
    # validation will be handled in the pydantic schema
    role = Column(String, default="user", nullable=False)

    cart_items = relationship("CartItem", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return "User: {}\nRole: {}".format(self.email, self.role)
