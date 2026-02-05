import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function ProtectedRoute({ children, requiredRole }: { children: React.ReactNode; requiredRole?: string }) {
  const auth = useAuth()

  if (!auth.isAuthenticated) {
    return <Navigate to="/login" />
  }

  if (requiredRole && auth.user?.role !== requiredRole) {
    return <Navigate to="/dashboard" />
  }

  return <>{children}</>
}
