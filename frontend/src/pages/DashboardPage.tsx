import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { TaskList } from '../components/TaskList'
import { FilterPanel, FilterState } from '../components/FilterPanel'
import apiClient from '../services/api'
import './DashboardPage.css'

export interface Task {
  id: string
  name: string
  priority: 'low' | 'medium' | 'high'
  owner_id: string
  project_id: string
  status: 'todo' | 'in_progress' | 'in_review' | 'done'
  delivery_date?: string
  position: number
  parent_task_id?: string
}

export function DashboardPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [tasks, setTasks] = useState<Task[]>([])
  const [projects, setProjects] = useState<Array<{ id: string; name: string }>>([])
  const [users, setUsers] = useState<Array<{ id: string; username: string }>>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState<FilterState>({})
  const [draggedTaskId, setDraggedTaskId] = useState<string | null>(null)

  // Fetch tasks on mount and when filters change
  useEffect(() => {
    fetchTasks()
    fetchProjects()
  }, [filters])

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()

      if (filters.owner_id) params.append('owner_id', filters.owner_id)
      if (filters.priority) params.append('priority', filters.priority)
      if (filters.status) params.append('status', filters.status)
      if (filters.project_id) params.append('project_id', filters.project_id)

      const response = await apiClient.get(`/tasks${params.size > 0 ? `?${params}` : ''}`)
      setTasks(response.data.tasks || [])
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load tasks')
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  const fetchProjects = async () => {
    try {
      const response = await apiClient.get('/projects')
      setProjects(response.data.projects || [])
    } catch (err) {
      // Projects optional for MVP
    }
  }

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters)
  }

  const handleTaskDragStart = (taskId: string, e: React.DragEvent) => {
    setDraggedTaskId(taskId)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleTaskDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    if (!draggedTaskId) return

    const dropY = e.clientY
    // Simple reordering by changing position
    // In full implementation, would calculate fractional position based on drop target

    try {
      await apiClient.patch(`/tasks/${draggedTaskId}/position`, {
        position: Math.random() * 100, // Placeholder - real implementation would calculate
      })
      setDraggedTaskId(null)
      await fetchTasks()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reorder task')
    }
  }

  const handleTaskDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>Dashboard</h1>
        </div>
        <div className="header-right">
          <span className="user-greeting">Welcome, {user?.display_name || user?.username}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <div className="dashboard-content">
        <FilterPanel onFilterChange={handleFilterChange} projects={projects} users={users} />

        <div className="tasks-section">
          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading-message">Loading tasks...</div>
          ) : (
            <TaskList
              tasks={tasks.map((task) => ({
                id: task.id,
                name: task.name,
                priority: task.priority,
                owner_id: task.owner_id,
                status: task.status,
                delivery_date: task.delivery_date,
                onDragStart: () => {}, // Handled by parent
              }))}
              onTaskDragStart={handleTaskDragStart}
              onTaskDrop={handleTaskDrop}
              onTaskDragOver={handleTaskDragOver}
            />
          )}
        </div>
      </div>
    </div>
  )
}
