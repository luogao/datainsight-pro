import { useState } from 'react'
import { Upload, BarChart3, FileText, Zap, CheckCircle2 } from 'lucide-react'
import FileUpload from './components/FileUpload'
import AnalysisForm from './components/AnalysisForm'
import ProgressDisplay from './components/ProgressDisplay'
import ReportViewer from './components/ReportViewer'
import { TaskStatus } from './types'

function App() {
  const [uploadedFile, setUploadedFile] = useState<{
    filename: string
    path: string
    size: number
    file_info?: any
  } | null>(null)
  const [task, setTask] = useState<TaskStatus | null>(null)
  const [report, setReport] = useState<string | null>(null)

  const handleFileUploaded = (fileData: any) => {
    setUploadedFile(fileData)
    setTask(null)
    setReport(null)
  }

  const handleAnalysisStarted = (taskData: TaskStatus) => {
    setTask(taskData)
    setReport(null)
  }

  const handleTaskCompleted = (reportContent: string) => {
    setReport(reportContent)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700/50 backdrop-blur-sm bg-slate-900/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-2 rounded-lg">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">DataInsight Pro</h1>
                <p className="text-xs text-slate-400">AI 智能数据分析</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Zap className="w-4 h-4 text-yellow-400" />
              <span>Powered by PandaAI & CrewAI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input */}
          <div className="lg:col-span-1 space-y-6">
            {/* Step 1: Upload File */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                  uploadedFile ? 'bg-green-500' : 'bg-slate-700'
                }`}>
                  {uploadedFile ? <CheckCircle2 className="w-4 h-4 text-white" /> : <Upload className="w-4 h-4 text-slate-400" />}
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">第 1 步：上传数据</h2>
                  <p className="text-sm text-slate-400">支持 CSV、JSON、Excel</p>
                </div>
              </div>
              <FileUpload onFileUploaded={handleFileUploaded} />
            </div>

            {/* Step 2: Configure Analysis */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                  uploadedFile ? 'bg-slate-700' : 'bg-slate-700'
                }`}>
                  <Zap className="w-4 h-4 text-slate-400" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">第 2 步：配置分析</h2>
                  <p className="text-sm text-slate-400">设置分析目标和深度</p>
                </div>
              </div>
              {uploadedFile ? (
                <AnalysisForm
                  uploadedFile={uploadedFile}
                  onAnalysisStarted={handleAnalysisStarted}
                />
              ) : (
                <div className="text-center py-8 text-slate-500">
                  <p>请先上传数据文件</p>
                </div>
              )}
            </div>

            {/* Progress */}
            {task && task.status !== 'completed' && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50 p-6">
                <ProgressDisplay task={task} onTaskCompleted={handleTaskCompleted} />
              </div>
            )}
          </div>

          {/* Right Column - Report */}
          <div className="lg:col-span-2">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50 p-6 h-full">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-slate-700">
                    <FileText className="w-4 h-4 text-slate-400" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-white">分析报告</h2>
                    <p className="text-sm text-slate-400">AI 生成的洞察和建议</p>
                  </div>
                </div>
                {report && (
                  <button
                    onClick={() => {
                      const blob = new Blob([report], { type: 'text/markdown' })
                      const url = URL.createObjectURL(blob)
                      const a = document.createElement('a')
                      a.href = url
                      a.download = 'analysis-report.md'
                      a.click()
                    }}
                    className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors"
                  >
                    下载报告
                  </button>
                )}
              </div>

              {report ? (
                <ReportViewer content={report} />
              ) : task?.status === 'running' ? (
                <div className="flex items-center justify-center py-20">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">分析进行中...</p>
                  </div>
                </div>
              ) : task?.status === 'failed' ? (
                <div className="flex items-center justify-center py-20">
                  <div className="text-center text-red-400">
                    <p>分析失败</p>
                    <p className="text-sm mt-2">{task.error}</p>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center py-20 text-slate-500">
                  <p>上传数据并开始分析，报告将在此显示</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700/50 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-500">
          <p>DataInsight Pro © 2024 - AI 驱动的智能数据分析平台</p>
        </div>
      </footer>
    </div>
  )
}

export default App
