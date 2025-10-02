from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from app.api.models.product import Product


class ProductRepository(BaseRepository[Product]):
    """
    Product repository class for CRUD operations on Product model.
    This class inherits from BaseRepository and provides specific methods for Product model.
    Attributes:
        model (Type[Product]): The SQLAlchemy Product model class.
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_by_name(self, name: str) -> Product:
        """Get a product by name.

        Args:
            name (str): The name of the product.

        Returns:
            Product: The product object if found, None otherwise.
        """
        return self.db.query(self.model).filter(self.model.name == name).first()

    def get_in_stock(self) -> list[Product]:
        """Get all products that are in stock.

        Returns:
            list[Product]: A list of products that have stock greater than 0.
        """
        return self.db.query(self.model).filter(self.model.stock > 0).all()

    def get_by_price_range(self, min_price: float, max_price: float) -> list[Product]:
        """Get products within a specific price range.

        Args:
            min_price (float): The minimum price.
            max_price (float): The maximum price.

        Returns:
            list[Product]: A list of products within the specified price range.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.price >= min_price, self.model.price <= max_price)
            .all()
        )
