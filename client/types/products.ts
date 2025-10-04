import { Decimal } from "decimal.js";

export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number; // We'll handle Decimal as number in the frontend
  stock: number;
}

export interface ProductListParams {
  q?: string;
  min_price?: number;
  max_price?: number;
  available?: boolean;
  page?: number;
  limit?: number;
}

export interface PaginatedProducts {
  total_items: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  items: Product[];
}

export interface ProductListResponse {
  status_code: number;
  message: string;
  data: PaginatedProducts;
}

export interface ProductResponse {
  status_code: number;
  message: string;
  data: Product;
}

export interface ProductCreateRequest {
  name: string;
  description?: string;
  price: number;
  stock: number;
}

export interface ProductUpdateRequest {
  name?: string;
  description?: string;
  price?: number;
  stock?: number;
}