import { useState } from 'react'
import { Zap, Send } from 'lucide-react'
import { apiService } from '../api'
import { TaskStatus } from '../types'

interface AnalysisFormProps {
  uploadedFile: {
    filename: string
    file_path: string
    size: number
    file_info?: any
  }
  onAnalysisStarted: (task: TaskStatus) => void
}

export default function AnalysisForm({ uploadedFile, onAnalysisStarted }: AnalysisFormProps) {
  const [goal, setGoal] = useState('')
  const [depth, setDepth] = useState<'quick' | 'standard' | 'deep'>('standard')
  const [outputFormat, setOutputFormat] = useState<'markdown' | 'json'>('markdown')
  const [starting, setStarting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!goal.trim()) {
      alert('请输入分析目标')
      return
    }

    try {
      setStarting(true)
      const task = await apiService.startAnalysis(
        goal,
        uploadedFile.file_path,
        depth,
        outputFormat
      )
      onAnalysisStarted(task)
    } catch (error) {
      console.error('启动分析失败:', error)
      alert('启动分析失败，请重试')
    } finally {
      setStarting(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* 文件信息 */}
      <div className="bg-slate-900/50 rounded-lg p-3 space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-400">文件名</span>
          <span className="text-white truncate max-w-[150px]">{uploadedFile.filename}</span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-400">大小</span>
          <span className="text-white">{formatFileSize(uploadedFile.size)}</span>
        </div>
        {uploadedFile.file_info && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-400">数据量</span>
            <span className="text-white">
              {uploadedFile.file_info.rows?.toLocaleString() || 'N/A'} 行 × {uploadedFile.file_info.columns || 'N/A'} 列
            </span>
          </div>
        )}
      </div>

      {/* 分析目标 */}
      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">
          分析目标
        </label>
        <textarea
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="例如：分析最近一个季度的销售数据，找出趋势和异常"
          className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
          rows={4}
        />
      </div>

      {/* 分析深度 */}
      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">
          分析深度
        </label>
        <div className="grid grid-cols-3 gap-2">
          {[
            { value: 'quick', label: '快速', desc: '基础统计' },
            { value: 'standard', label: '标准', desc: '完整分析' },
            { value: 'deep', label: '深入', desc: '预测洞察' }
          ].map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => setDepth(option.value as any)}
              className={`
                px-3 py-3 rounded-lg text-sm text-left transition-all
                ${depth === option.value
                  ? 'bg-primary-600 text-white ring-2 ring-primary-500 ring-offset-2 ring-offset-slate-800'
                  : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                }
              `}
            >
              <div className="font-medium">{option.label}</div>
              <div className="text-xs opacity-75">{option.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* 输出格式 */}
      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">
          输出格式
        </label>
        <div className="grid grid-cols-2 gap-2">
          {[
            { value: 'markdown', label: 'Markdown' },
            { value: 'json', label: 'JSON' }
          ].map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => setOutputFormat(option.value as any)}
              className={`
                px-3 py-2 rounded-lg text-sm transition-all
                ${outputFormat === option.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                }
              `}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* 提交按钮 */}
      <button
        type="submit"
        disabled={starting || !goal.trim()}
        className={`
          w-full px-4 py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800
          text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2
          ${starting || !goal.trim() ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <Zap className="w-5 h-5" />
        <span>{starting ? '启动中...' : '开始分析'}</span>
      </button>
    </form>
  )
}
