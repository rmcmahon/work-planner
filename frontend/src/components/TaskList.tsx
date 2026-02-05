import React from 'react'
import { TaskCard, TaskCardProps } from './TaskCard'
import './TaskList.css'

export interface TaskListProps {
  tasks: TaskCardProps[]
  onTaskDragStart: (taskId: string, e: React.DragEvent) => void
  onTaskDrop: (e: React.DragEvent) => void
  onTaskDragOver: (e: React.DragEvent) => void
}

export function TaskList({ tasks, onTaskDragStart, onTaskDrop, onTaskDragOver }: TaskListProps) {
  if (tasks.length === 0) {
    return <div className="task-list-empty">No tasks found</div>
  }

  return (
    <div className="task-list" onDrop={onTaskDrop} onDragOver={onTaskDragOver} role="main">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          {...task}
          onDragStart={(e) => onTaskDragStart(task.id, e)}
        />
      ))}
    </div>
  )
}
