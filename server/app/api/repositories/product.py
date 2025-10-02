from sqlalchemy.orm import Session, Query
from typing import Optional
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

    # filter methods that can be chained together in the service layer

    def base_query(self) -> Query[Product]:
        """Create a base query for the Product model.

        Returns:
            Query[Product]: A SQLAlchemy query object for the Product model.
        """
        return self.db.query(self.model)

    def search_by_name(
        self, query: Query[Product], name: Optional[str]
    ) -> Query[Product]:
        """Search products by name (case-insensitive).

        Args:
            name (str): The name or partial name to search for.

        Returns:
            Query[Product]: A SQLAlchemy query object with the applied filter.
        """
        if name:
            return query.filter(self.model.name.ilike(f"%{name}%"))
        return query

    def filter_by_stock(
        self, query: Query[Product], in_stock: Optional[bool]
    ) -> Query[Product]:
        """Filter products by stock availability.

        Args:
            in_stock (bool): If True, filter products that are in stock (stock > 0).
                             If False, filter products that are out of stock (stock == 0).

        Returns:
            Query[Product]: A SQLAlchemy query object with the applied filter.
        """
        if in_stock is not None:
            if in_stock:
                return query.filter(self.model.stock > 0)
            else:
                return query.filter(self.model.stock == 0)
        return query

    def get_by_price_range(
        self, query: Query[Product], min_price: float, max_price: float
    ) -> Query[Product]:
        """Get products within a specific price range.

        Args:
            min_price (float): The minimum price.
            max_price (float): The maximum price.

        Returns:
            Query[Product]: A SQLAlchemy query object with the applied price range filter.
        """

        return query.filter(
            self.model.price >= min_price, self.model.price <= max_price
        )