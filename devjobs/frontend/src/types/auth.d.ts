export interface LoginResponse {
  username: string
  refresh: string
  access: string
}

export interface RefreshResponse {
  access: string
  refresh: string
}
