import React from 'react'
import './TaskCard.css'

export interface TaskCardProps {
  id: string
  name: string
  priority: 'low' | 'medium' | 'high'
  owner_id: string
  status: 'todo' | 'in_progress' | 'in_review' | 'done'
  delivery_date?: string
  onDragStart: (e: React.DragEvent) => void
}

export function TaskCard({ id, name, priority, status, delivery_date, onDragStart }: TaskCardProps) {
  const priorityClass = `priority-${priority}`
  const statusClass = `status-${status}`

  const formatDate = (date?: string) => {
    if (!date) return ''
    return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <div
      className="task-card"
      draggable
      onDragStart={onDragStart}
      data-task-id={id}
      role="article"
      aria-label={`Task: ${name}`}
    >
      <div className="task-header">
        <h3 className="task-name">{name}</h3>
        <span className={`priority-badge ${priorityClass}`}>{priority}</span>
      </div>

      <div className="task-meta">
        <span className={`status-badge ${statusClass}`}>{status.replace('_', ' ')}</span>
        {delivery_date && <span className="delivery-date">{formatDate(delivery_date)}</span>}
      </div>
    </div>
  )
}
