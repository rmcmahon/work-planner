import { useContext, ReactNode, createContext } from 'react'

interface AuthContextType {
  isAuthenticated: boolean
  user: null | { id: string; username: string; role: string }
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  return <AuthContext.Provider value={{ isAuthenticated: false, user: null, login: async () => {}, logout: () => {} }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
