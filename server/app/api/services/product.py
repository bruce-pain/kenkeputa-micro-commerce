from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.products import schemas
from app.core.base.schema import PaginatedResponse
from app.api.models.product import Product
from app.api.repositories.product import ProductRepository
from app.utils.logger import logger


class ProductService:
    """
    Product service class for handling product-related operations.
    This class provides methods for creating, updating, retrieving, and listing products.
    """

    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, schema: schemas.ProductCreateRequest) -> Product:
        """Creates a new product
        Args:
            schema (schemas.ProductCreateRequest): Product creation schema
        Returns:
            Product: Product object for the newly created product
        """
        # check if product with name already exists
        if self.repository.get_by_name(schema.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists!",
            )

        product = Product(**schema.model_dump())

        try:
            logger.info(f"Creating product with name: {product.name}")
            return self.repository.create(product)
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating product",
            )

    def retrieve_product(self, product_id: str) -> Product:
        """Retrieves a product by its ID
        Args:
            product_id (str): The ID of the product to retrieve
        Returns:
            Product: The retrieved product object
        """
        product = self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!",
            )
        return product

    def update_product(
        self, product_id: str, schema: schemas.ProductUpdateRequest
    ) -> Product:
        """Updates a product by its ID
        Args:
            product_id (str): The ID of the product to update
            schema (schemas.ProductUpdateRequest): Product update schema
        Returns:
            Product: The updated product object
        """
        product = self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!",
            )

        # check if product with name already exists
        if schema.name and schema.name != product.name:
            if self.repository.get_by_name(schema.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product with this name already exists!",
                )

        # update only the fields that are set in the schema
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        try:
            logger.info(f"Updating product with id: {product.id}")
            return self.repository.update(product)
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating product",
            )

    def delete_product(self, product_id: str) -> None:
        """Deletes a product by its ID
        Args:
            product_id (str): The ID of the product to delete
        Returns:
            None
        """
        product = self.repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!",
            )

        try:
            logger.info(f"Deleting product with id: {product.id}")
            self.repository.delete(product_id)
        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting product",
            )

    def list_products(
        self,
        name: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse:
        """Lists products with optional filtering and pagination
        Args:
            name (str | None): Optional name filter (case-insensitive, partial match)
            in_stock (bool | None): Optional stock availability filter
            min_price (float | None): Optional minimum price filter
            max_price (float | None): Optional maximum price filter
            page (int): Page number for pagination (default is 1)
            page_size (int): Number of items per page for pagination (default is 10)
        Returns:
            list[Product]: A list of products matching the filters and pagination
        """

        query = self.repository.base_query()

        # apply filters
        query = self.repository.search_by_name(query, name)
        query = self.repository.filter_by_stock(query, in_stock)

        # price range filter
        if min_price is not None and max_price is not None:
            query = self.repository.get_by_price_range(query, min_price, max_price)
        if min_price is not None and max_price is None:
            query = self.repository.get_by_price_range(query, min_price, float("inf"))
        if min_price is None and max_price is not None:
            query = self.repository.get_by_price_range(query, 0, max_price)

        # apply pagination and return
        return self.repository.paginate(query, page, page_size)
