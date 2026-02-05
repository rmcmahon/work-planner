import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { DashboardPage } from '../../pages/DashboardPage'
import { AuthProvider } from '../../context/AuthContext'

describe('DashboardPage', () => {
  const renderDashboard = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <DashboardPage />
        </AuthProvider>
      </BrowserRouter>,
    )
  }

  it('should render dashboard header', () => {
    renderDashboard()
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('should display logout button', () => {
    renderDashboard()
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument()
  })

  it('should display welcome message with user name', () => {
    renderDashboard()
    const welcomeText = screen.getByText(/welcome/i)
    expect(welcomeText).toBeInTheDocument()
  })

  // T028: Integration test for Dashboard page render with task list (placeholder)
  it('should render task list placeholder', () => {
    renderDashboard()
    expect(screen.getByText(/tasks/i)).toBeInTheDocument()
  })
})
