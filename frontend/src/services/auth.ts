import apiClient from './api'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: UserInfo
}

export interface UserInfo {
  id: string
  username: string
  email: string
  display_name?: string
  role: string
  is_active: boolean
}

export const authService = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/login', credentials)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('refresh_token', response.data.refresh_token)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  getCurrentUser: (): UserInfo | null => {
    const user = localStorage.getItem('current_user')
    return user ? JSON.parse(user) : null
  },

  setCurrentUser: (user: UserInfo) => {
    localStorage.setItem('current_user', JSON.stringify(user))
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token')
  },
}
