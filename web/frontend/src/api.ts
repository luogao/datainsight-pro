import axios from 'axios'
import { TaskStatus, UploadedFile } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // 上传文件
  async uploadFile(file: File): Promise<UploadedFile> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  },

  // 启动分析
  async startAnalysis(
    goal: string,
    datasetPath: string,
    depth: string = 'standard',
    outputFormat: string = 'markdown'
  ): Promise<TaskStatus> {
    const formData = new FormData()
    formData.append('goal', goal)
    formData.append('dataset_path', datasetPath)
    formData.append('depth', depth)
    formData.append('output_format', outputFormat)

    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  },

  // 获取任务状态
  async getTaskStatus(taskId: string): Promise<TaskStatus> {
    const response = await api.get(`/tasks/${taskId}`)
    return response.data
  },

  // 获取报告
  async getReport(taskId: string): Promise<{ task_id: string; content: string; format: string }> {
    const response = await api.get(`/reports/${taskId}`)
    return response.data
  },

  // 健康检查
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await api.get('/health')
    return response.data
  },

  // 获取示例数据
  async getSampleData(): Promise<{ samples: any[] }> {
    const response = await api.get('/sample-data')
    return response.data
  },
}
