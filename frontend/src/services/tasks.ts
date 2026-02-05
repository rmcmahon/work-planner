import apiClient from './api'

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

export interface TasksResponse {
  tasks: Task[]
  total: number
}

export const tasksService = {
  getTasks: async (filters?: Record<string, any>): Promise<Task[]> => {
    const params = new URLSearchParams()
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value)
      })
    }
    const response = await apiClient.get<TasksResponse>(
      `/tasks${params.size > 0 ? `?${params}` : ''}`,
    )
    return response.data.tasks
  },

  getTask: async (id: string): Promise<Task> => {
    const response = await apiClient.get<Task>(`/tasks/${id}`)
    return response.data
  },

  createTask: async (task: Partial<Task>): Promise<Task> => {
    const response = await apiClient.post<Task>('/tasks', task)
    return response.data
  },

  updateTask: async (id: string, task: Partial<Task>): Promise<Task> => {
    const response = await apiClient.patch<Task>(`/tasks/${id}`, task)
    return response.data
  },

  reorderTask: async (
    id: string,
    position: number,
    parent_task_id?: string,
  ): Promise<Task> => {
    const response = await apiClient.patch<Task>(`/tasks/${id}/position`, {
      position,
      parent_task_id,
    })
    return response.data
  },

  deleteTask: async (id: string): Promise<void> => {
    await apiClient.delete(`/tasks/${id}`)
  },
}
