import { RegisterRequest, LoginRequest, AuthResponse, ApiError } from "@/types/auth";
import axios, { AxiosRequestConfig } from "axios";

const API_BASE_URL = "http://192.168.99.51:8000";


class ApiService {
  private async request<T>(
    endpoint: string,
    options: AxiosRequestConfig = {}
  ): Promise<T> {
    const config: AxiosRequestConfig = {
      ...options,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        "Content-Type": "application/json",
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
}

export const apiService = new ApiService();