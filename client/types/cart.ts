export interface CartProduct {
  id: string;
  name: string;
  unit_price: number;
  stock: number;
}

export interface CartItem {
  id: string;
  user_id: string;
  product_id: string;
  quantity: number;
  total_price: number;
  product: CartProduct;
  created_at: string;
}

export interface CartItemListData {
  total_cart_value: number;
  items_count: number;
  items: CartItem[];
}

export interface CartItemListResponse {
  status_code: number;
  message: string;
  data: CartItemListData;
}

export interface CartItemResponse {
  status_code: number;
  message: string;
  data: CartItem;
}

export interface AddToCartRequest {
  product_id: string;
  quantity: number;
}

export interface UpdateCartItemRequest {
  quantity: number;
}