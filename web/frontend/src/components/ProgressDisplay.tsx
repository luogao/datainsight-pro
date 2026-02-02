import { useEffect, useState } from 'react'
import { Clock, CheckCircle2, AlertCircle } from 'lucide-react'
import { apiService } from '../api'
import { TaskStatus } from '../types'

interface ProgressDisplayProps {
  task: TaskStatus
  onTaskCompleted: (report: string) => void
}

export default function ProgressDisplay({ task, onTaskCompleted }: ProgressDisplayProps) {
  const [currentTask, setCurrentTask] = useState(task)

  useEffect(() => {
    const pollTask = async () => {
      try {
        const updatedTask = await apiService.getTaskStatus(task.task_id)
        setCurrentTask(updatedTask)

        if (updatedTask.status === 'completed') {
          if (updatedTask.result?.report_content) {
            const content = typeof updatedTask.result.report_content === 'string'
              ? updatedTask.result.report_content
              : JSON.stringify(updatedTask.result.report_content, null, 2)
            onTaskCompleted(content)
          }
        }
      } catch (error) {
        console.error('获取任务状态失败:', error)
      }
    }

    if (task.status === 'running') {
      const interval = setInterval(pollTask, 2000)
      return () => clearInterval(interval)
    }
  }, [task.task_id, task.status, onTaskCompleted])

  const getStatusIcon = () => {
    switch (currentTask.status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-500" />
      default:
        return <Clock className="w-5 h-5 text-yellow-500 animate-pulse" />
    }
  }

  const getStatusText = () => {
    switch (currentTask.status) {
      case 'pending':
        return '等待中...'
      case 'running':
        return '分析进行中'
      case 'completed':
        return '分析完成'
      case 'failed':
        return '分析失败'
    }
  }

  const formatTime = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="space-y-4">
      {/* 状态 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {getStatusIcon()}
          <div>
            <p className="text-white font-medium">{getStatusText()}</p>
            <p className="text-sm text-slate-400">{currentTask.current_step}</p>
          </div>
        </div>
        <span className="text-sm text-slate-400">
          {formatTime(currentTask.updated_at)}
        </span>
      </div>

      {/* 进度条 */}
      {currentTask.status === 'running' && (
        <div className="space-y-2">
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500 ease-out"
              style={{ width: `${currentTask.progress}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-slate-400">
            <span>分析进度</span>
            <span>{currentTask.progress}%</span>
          </div>
        </div>
      )}

      {/* 错误信息 */}
      {currentTask.status === 'failed' && currentTask.error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-3">
          <p className="text-sm text-red-400">{currentTask.error}</p>
        </div>
      )}

      {/* 任务 ID */}
      <div className="text-xs text-slate-500 font-mono">
        Task ID: {currentTask.task_id}
      </div>
    </div>
  )
}
