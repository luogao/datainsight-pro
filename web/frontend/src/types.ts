export interface TaskStatus {
  task_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  current_step: string
  result?: {
    report_path?: string
    report_content?: any
    output_format?: string
  }
  error?: string
  created_at: string
  updated_at: string
}

export interface UploadedFile {
  filename: string
  file_path: string
  size: number
  file_info?: {
    rows?: number
    columns?: number
    column_names?: string[]
    preview?: any[]
  }
}

export interface AnalysisRequest {
  goal: string
  dataset_path: string
  depth: 'quick' | 'standard' | 'deep'
  output_format: 'markdown' | 'json'
}
