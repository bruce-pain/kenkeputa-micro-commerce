import { RegisterRequest, LoginRequest, AuthResponse, ApiError } from "@/types/auth";
import {
  ProductListParams,
  ProductListResponse,
  ProductResponse,
  ProductCreateRequest,
  ProductUpdateRequest,
} from "@/types/product";
import axios, { AxiosRequestConfig } from "axios";
import { storage } from "@/utils/storage";

const API_BASE_URL = "http://192.168.99.51:8000";


class ApiService {
  private async request<T>(
    endpoint: string,
    options: AxiosRequestConfig = {}
  ): Promise<T> {
    const token = await storage.getAccessToken();
    
    const config: AxiosRequestConfig = {
      ...options,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    };

    try {
      const response = await axios(config);
      return response.data as T;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw error.response.data as ApiError;
      }
      throw error;
    }
  }

  // Auth methods
  async register(data: RegisterRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>("/api/v1/auth/register", {
      method: "POST",
      data,
    });
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>("/api/v1/auth/login", {
      method: "POST",
      data,
    });
  }

  // Product methods
  async getProducts(params: ProductListParams): Promise<ProductListResponse> {
    const queryParams = new URLSearchParams();
    
    if (params.q) queryParams.append("q", params.q);
    if (params.min_price !== undefined) queryParams.append("min_price", params.min_price.toString());
    if (params.max_price !== undefined) queryParams.append("max_price", params.max_price.toString());
    if (params.available !== undefined) queryParams.append("available", params.available.toString());
    if (params.page) queryParams.append("page", params.page.toString());
    if (params.limit) queryParams.append("limit", params.limit.toString());

    const queryString = queryParams.toString();
    const endpoint = `/api/v1/products${queryString ? `?${queryString}` : ""}`;

    return this.request<ProductListResponse>(endpoint, {
      method: "GET",
    });
  }

  async getProduct(productId: string): Promise<ProductResponse> {
    return this.request<ProductResponse>(`/api/v1/products/${productId}`, {
      method: "GET",
    });
  }

  async createProduct(data: ProductCreateRequest): Promise<ProductResponse> {
    return this.request<ProductResponse>("/api/v1/products", {
      method: "POST",
      data,
    });
  }

  async updateProduct(
    productId: string,
    data: ProductUpdateRequest
  ): Promise<ProductResponse> {
    return this.request<ProductResponse>(`/api/v1/products/${productId}`, {
      method: "PUT",
      data,
    });
  }

  async deleteProduct(productId: string): Promise<void> {
    return this.request<void>(`/api/v1/products/${productId}`, {
      method: "DELETE",
    });
  }
}

export const apiService = new ApiService();