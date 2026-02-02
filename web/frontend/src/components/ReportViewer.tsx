import { useState } from 'react'
import { FileText, Eye, Code, Download } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface ReportViewerProps {
  content: string
}

export default function ReportViewer({ content }: ReportViewerProps) {
  const [viewMode, setViewMode] = useState<'rendered' | 'raw'>('rendered')

  return (
    <div className="space-y-4">
      {/* 视图切换 */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => setViewMode('rendered')}
          className={`
            px-3 py-2 rounded-lg text-sm flex items-center gap-2 transition-all
            ${viewMode === 'rendered'
              ? 'bg-primary-600 text-white'
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
            }
          `}
        >
          <Eye className="w-4 h-4" />
          <span>预览</span>
        </button>
        <button
          onClick={() => setViewMode('raw')}
          className={`
            px-3 py-2 rounded-lg text-sm flex items-center gap-2 transition-all
            ${viewMode === 'raw'
              ? 'bg-primary-600 text-white'
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
            }
          `}
        >
          <Code className="w-4 h-4" />
          <span>源码</span>
        </button>
      </div>

      {/* 内容区域 */}
      <div className="bg-slate-900/50 rounded-lg border border-slate-700/50 overflow-hidden">
        {viewMode === 'rendered' ? (
          <div className="p-6 prose prose-invert prose-slate max-w-none">
            <ReactMarkdown
              components={{
                h1: ({ node, ...props }) => <h1 className="text-2xl font-bold text-white mb-4" {...props} />,
                h2: ({ node, ...props }) => <h2 className="text-xl font-bold text-white mt-6 mb-3" {...props} />,
                h3: ({ node, ...props }) => <h3 className="text-lg font-semibold text-white mt-4 mb-2" {...props} />,
                p: ({ node, ...props }) => <p className="text-slate-300 mb-4 leading-relaxed" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc list-inside text-slate-300 mb-4 space-y-1" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal list-inside text-slate-300 mb-4 space-y-1" {...props} />,
                li: ({ node, ...props }) => <li className="text-slate-300" {...props} />,
                code: ({ node, inline, ...props }: any) =>
                  inline ? (
                    <code className="bg-slate-700 px-2 py-1 rounded text-sm text-primary-300" {...props} />
                  ) : (
                    <code className="block bg-slate-800 p-4 rounded-lg text-sm overflow-x-auto" {...props} />
                  ),
                blockquote: ({ node, ...props }) => (
                  <blockquote className="border-l-4 border-primary-500 pl-4 italic text-slate-400 my-4" {...props} />
                ),
                table: ({ node, ...props }) => (
                  <div className="overflow-x-auto my-4">
                    <table className="min-w-full divide-y divide-slate-700" {...props} />
                  </div>
                ),
                thead: ({ node, ...props }) => <thead className="bg-slate-800" {...props} />,
                tbody: ({ node, ...props }) => <tbody className="divide-y divide-slate-700" {...props} />,
                tr: ({ node, ...props }) => <tr className="hover:bg-slate-800/50" {...props} />,
                th: ({ node, ...props }) => (
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider" {...props} />
                ),
                td: ({ node, ...props }) => <td className="px-4 py-3 text-sm text-slate-300" {...props} />,
                strong: ({ node, ...props }) => <strong className="text-white font-semibold" {...props} />,
                a: ({ node, ...props }) => (
                  <a className="text-primary-400 hover:text-primary-300 underline" {...props} />
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        ) : (
          <pre className="p-6 overflow-x-auto text-sm text-slate-300 font-mono">
            {content}
          </pre>
        )}
      </div>
    </div>
  )
}
