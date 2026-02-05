import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react'
import { authService, UserInfo } from '../services/auth'

interface AuthContextType {
  isAuthenticated: boolean
  user: UserInfo | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<UserInfo | null>(null)

  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const savedUser = authService.getCurrentUser()
    if (token && savedUser) {
      setIsAuthenticated(true)
      setUser(savedUser)
    }
  }, [])

  const login = async (username: string, password: string) => {
    const response = await authService.login({ username, password })
    authService.setCurrentUser(response.user)
    setUser(response.user)
    setIsAuthenticated(true)
  }

  const logout = () => {
    authService.logout()
    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
