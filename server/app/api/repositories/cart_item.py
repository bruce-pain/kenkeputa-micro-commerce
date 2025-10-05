from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.base.repository import BaseRepository
from app.api.models.cart_item import CartItem
from app.api.models.product import Product


class CartItemRepository(BaseRepository[CartItem]):
    """
    CartItem repository class for CRUD operations on CartItem model.
    This class inherits from BaseRepository and provides specific methods for CartItem model.
    Attributes:
        model (Type[CartItem]): The SQLAlchemy CartItem model class.
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        super().__init__(CartItem, db)

    def get_user_cart_items(self, user_id: str) -> List[tuple[CartItem, Product]]:
        """Get all cart items for a specific user by user_id.

        Args:
            user_id (str): The ID of the user.

        Returns:
            List[Tuple[CartItem, Product]]: A list of tuples containing CartItem and associated Product objects.
        """
        return (
            self.db.query(self.model, Product)
            .filter(self.model.user_id == user_id)
            .join(Product, Product.id == self.model.product_id)
            .all()
        )

    def get_product_from_user_cart(
        self, user_id: str, product_id: str
    ) -> Optional[CartItem]:
        """Get a specific cart item by user_id and product_id.

        This is needed to check if a product already exists in the user's cart
        before adding a new item or updating quantity.

        Args:
            user_id (str): The ID of the user.
            product_id (str): The ID of the product.

        Returns:
            CartItem | None: The cart item if found, None otherwise.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.product_id == product_id)
            .first()
        )

    def get_user_cart_item(self, item_id: str, user_id: str) -> Optional[CartItem]:
        """Get a cart item by its ID and verify it belongs to the user.

        This is needed for security - to ensure users can only update/delete
        their own cart items.

        Args:
            item_id (str): The ID of the cart item.
            user_id (str): The ID of the user.

        Returns:
        Optional[CartItem]: The cart item if found and belongs to user, None otherwise.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.id == item_id, self.model.user_id == user_id)
            .first()
        )

    def update_cart_item_quantity(
        self, item_id: str, user_id: str, quantity: int
    ) -> Optional[CartItem]:
        """Update the quantity of a cart item for a specific user.

        This method retrieves the cart item for the user and updates its quantity.

        Args:
            item_id (str): The ID of the cart item.
            user_id (str): The ID of the user.
            quantity (int): The new quantity to set.

        Returns:
            Optional[CartItem]: The updated cart item if found, None otherwise.
        """
        cart_item = self.get_user_cart_item(item_id, user_id)
        if cart_item:
            cart_item.quantity = quantity
            self.db.commit()
            self.db.refresh(cart_item)
            return cart_item
        return None

    def delete_cart_items_by_user_id(self, user_id: str) -> None:
        """Delete all cart items for a specific user by user_id.

        Args:
            user_id (str): The ID of the user.
        """
        self.db.query(self.model).filter(self.model.user_id == user_id).delete()
        self.db.commit()
