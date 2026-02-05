import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import './App.css'

// Placeholder pages - to be implemented in Phase 3
const LoginPage = () => <div>Login Page - Coming Soon</div>
const DashboardPage = () => <div>Dashboard - Coming Soon</div>
const AdminPage = () => <div>Admin Page - Coming Soon</div>

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
