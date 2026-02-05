import apiClient from './api'

export interface Project {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface ProjectsResponse {
  projects: Project[]
  total: number
}

export const projectsService = {
  getProjects: async (): Promise<Project[]> => {
    const response = await apiClient.get<ProjectsResponse>('/projects')
    return response.data.projects
  },

  getProject: async (id: string): Promise<Project> => {
    const response = await apiClient.get<Project>(`/projects/${id}`)
    return response.data
  },

  createProject: async (project: Partial<Project>): Promise<Project> => {
    const response = await apiClient.post<Project>('/projects', project)
    return response.data
  },

  updateProject: async (id: string, project: Partial<Project>): Promise<Project> => {
    const response = await apiClient.patch<Project>(`/projects/${id}`, project)
    return response.data
  },

  deleteProject: async (id: string): Promise<void> => {
    await apiClient.delete(`/projects/${id}`)
  },
}
