export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponseData {
  id: string;
  email: string;
  role: "admin" | "user";
}

export interface AuthResponse {
  status_code: number;
  message: string;
  access_token: string;
  refresh_token: string;
  data: AuthResponseData;
}

export interface ApiError {
  status: boolean;
  status_code: number;
  message: string;
  errors?: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}