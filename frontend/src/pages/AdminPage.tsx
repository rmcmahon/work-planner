import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function AdminPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="admin-container">
      <header className="admin-header">
        <h1>Admin Panel</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="admin-content">
        <div className="placeholder">
          <h2>Admin Tools</h2>
          <p>User and project management will appear here in Phase 5</p>
        </div>
      </main>
    </div>
  )
}
