import React, { useState } from 'react'
import './FilterPanel.css'

export interface FilterState {
  priority?: string
  status?: string
  owner_id?: string
  project_id?: string
}

export interface FilterPanelProps {
  onFilterChange: (filters: FilterState) => void
  projects: Array<{ id: string; name: string }>
  users: Array<{ id: string; username: string }>
}

export function FilterPanel({ onFilterChange, projects = [], users = [] }: FilterPanelProps) {
  const [filters, setFilters] = useState<FilterState>({})

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    const newFilters = { ...filters, [key]: value || undefined }
    setFilters(newFilters)
    onFilterChange(newFilters)
  }

  const handleReset = () => {
    setFilters({})
    onFilterChange({})
  }

  return (
    <div className="filter-panel">
      <div className="filter-header">
        <h3>Filters</h3>
        <button onClick={handleReset} className="reset-button">
          Reset
        </button>
      </div>

      <div className="filter-group">
        <label htmlFor="priority-filter">Priority</label>
        <select
          id="priority-filter"
          value={filters.priority || ''}
          onChange={(e) => handleFilterChange('priority', e.target.value)}
        >
          <option value="">All Priorities</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="status-filter">Status</label>
        <select
          id="status-filter"
          value={filters.status || ''}
          onChange={(e) => handleFilterChange('status', e.target.value)}
        >
          <option value="">All Statuses</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="in_review">In Review</option>
          <option value="done">Done</option>
        </select>
      </div>

      {users.length > 0 && (
        <div className="filter-group">
          <label htmlFor="owner-filter">Owner</label>
          <select
            id="owner-filter"
            value={filters.owner_id || ''}
            onChange={(e) => handleFilterChange('owner_id', e.target.value)}
          >
            <option value="">All Users</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>
      )}

      {projects.length > 0 && (
        <div className="filter-group">
          <label htmlFor="project-filter">Project</label>
          <select
            id="project-filter"
            value={filters.project_id || ''}
            onChange={(e) => handleFilterChange('project_id', e.target.value)}
          >
            <option value="">All Projects</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  )
}
