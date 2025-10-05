from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.cart_items import schemas
from app.api.models.cart_item import CartItem
from app.api.models.user import User
from app.api.repositories.cart_item import CartItemRepository
from app.api.repositories.product import ProductRepository
from app.utils.logger import logger


class CartItemService:
    """
    CartItem service class for handling cart item-related operations.
    This class provides methods for adding, updating, retrieving, and deleting cart items.
    """

    def __init__(self, db: Session):
        self.repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)

    def add_item_to_cart(
        self, current_user: User, schema: schemas.CartItemCreateRequest
    ) -> schemas.CartItemResponseData:
        """
        Adds an item to the user's cart. If the item already exists in the cart, it updates the quantity.
        
        Args:
            current_user (User): The currently authenticated user.
            schema (schemas.CartItemCreateRequest): The cart item creation schema

        Returns:
            schemas.CartItemResponse: The response schema for the cart item.
        """
        # Check if the product exists
        product = self.product_repository.get(schema.product_id)
        if not product:
            logger.error(f"Product with ID {schema.product_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        # Validate quantity
        if schema.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

        # Check if product already exists in user's cart
        cart_item = self.repository.get_product_from_user_cart(
            current_user.id, schema.product_id
        )

        if cart_item:
            # Calculate new total quantity
            new_quantity = cart_item.quantity + schema.quantity
            
            # Check if new quantity exceeds available stock
            if new_quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Quantity exceeds available stock. Available: {product.stock}, In cart: {cart_item.quantity}, Requested: {schema.quantity}",
                )
            
            cart_item.quantity = new_quantity
            try:
                logger.info(f"Updating cart item quantity for user {current_user.id}, product {schema.product_id}")
                self.repository.update(cart_item)
            except Exception as e:
                logger.error(f"Error updating cart item: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error updating cart item",
                )
        else:
            # Check if quantity is less than or equal to stock
            if schema.quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Quantity exceeds available stock. Available: {product.stock}",
                )
            
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=schema.product_id,
                quantity=schema.quantity,
            )
            try:
                logger.info(f"Adding item to cart for user {current_user.id}, product {schema.product_id}")
                cart_item = self.repository.create(cart_item)
            except Exception as e:
                logger.error(f"Error creating cart item: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error adding item to cart",
                )

        total_price = float(product.price) * cart_item.quantity
        return schemas.CartItemResponseData(
            id=cart_item.id,
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            total_price=total_price,
            product=schemas.CartProduct(
                id=product.id, 
                name=product.name, 
                unit_price=float(product.price),
                stock=product.stock
            ),
            created_at=str(cart_item.created_at),
        )

    def get_user_cart(self, current_user: User) -> schemas.CartItemListResponseData:
        """
        Retrieves all cart items for the current user along with the total cart value.
        
        Args:
            current_user (User): The currently authenticated user.

        Returns:
            schemas.CartItemListResponse: The response schema for the cart item list.
        """
        cart_items = self.repository.get_user_cart_items(current_user.id)
        total_cart_value = 0.0
        cart_items_response = []

        for cart_item, product in cart_items:
            total_price = float(product.price) * cart_item.quantity
            total_cart_value += total_price
            cart_items_response.append(
                schemas.CartItemResponseData(
                    id=cart_item.id,
                    user_id=cart_item.user_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    total_price=total_price,
                    product=schemas.CartProduct(
                        id=product.id,
                        name=product.name,
                        unit_price=float(product.price),
                        stock=product.stock
                    ),
                    created_at=str(cart_item.created_at),
                )
            )

        logger.info(f"Retrieved cart for user {current_user.id} with {len(cart_items_response)} items")
        return schemas.CartItemListResponseData(
            total_cart_value=total_cart_value, 
            items_count=len(cart_items_response),
            items=cart_items_response
        )

    def update_cart_item(
        self, item_id: str, current_user: User, schema: schemas.CartItemUpdateRequest
    ) -> schemas.CartItemResponseData:
        """
        Updates the quantity of a cart item for the current user.
        
        Args:
            item_id (str): The ID of the cart item to update.
            current_user (User): The currently authenticated user.
            schema (schemas.CartItemUpdateRequest): The cart item update schema.

        Returns:
            schemas.CartItemResponse: The updated cart item response.
        """
        # Verify cart item exists and belongs to user
        cart_item = self.repository.get_user_cart_item(item_id, current_user.id)
        if not cart_item:
            logger.error(f"Cart item {item_id} not found for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found or does not belong to you"
            )

        # Validate quantity
        if schema.quantity is not None and schema.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

        # Check if product still exists
        product = self.product_repository.get(cart_item.product_id)
        if not product:
            logger.error(f"Product {cart_item.product_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Validate stock availability
        if schema.quantity is not None and schema.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantity exceeds available stock. Available: {product.stock}",
            )

        # Update quantity
        if schema.quantity is not None:
            cart_item.quantity = schema.quantity
        
        try:
            logger.info(f"Updating cart item {item_id} for user {current_user.id}")
            self.repository.update(cart_item)
        except Exception as e:
            logger.error(f"Error updating cart item: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating cart item",
            )

        total_price = float(product.price) * cart_item.quantity
        return schemas.CartItemResponseData(
            id=cart_item.id,
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            total_price=total_price,
            product=schemas.CartProduct(
                id=product.id, 
                name=product.name, 
                unit_price=float(product.price),
                stock=product.stock
            ),
            created_at=str(cart_item.created_at),
        )

    def remove_cart_item(self, item_id: str, current_user: User) -> None:
        """
        Removes a specific cart item for the current user.
        
        Args:
            item_id (str): The ID of the cart item to remove.
            current_user (User): The currently authenticated user.
        """
        # Verify cart item exists and belongs to user
        cart_item = self.repository.get_user_cart_item(item_id, current_user.id)
        if not cart_item:
            logger.error(f"Cart item {item_id} not found for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found or does not belong to you"
            )

        try:
            logger.info(f"Removing cart item {item_id} for user {current_user.id}")
            self.repository.delete(item_id)
        except Exception as e:
            logger.error(f"Error removing cart item: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error removing cart item",
            )

    def clear_user_cart(self, current_user: User) -> None:
        """
        Clears all cart items for the current user.
        
        Args:
            current_user (User): The currently authenticated user.
        """
        try:
            logger.info(f"Clearing cart for user {current_user.id}")
            self.repository.delete_cart_items_by_user_id(current_user.id)
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error clearing cart",
            )
