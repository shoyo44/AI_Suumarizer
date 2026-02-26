import { useState, useRef, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../lib/api'
import type { Usecase } from '../lib/api'
import { parseFile, validateFile } from '../lib/fileParser'
import './Analyzer.css'
interface AnalyzerProps {
  usecases: Usecase[]
  onAnalysisComplete: () => void
  initialText?: string
  initialUsecase?: string
}

export default function Analyzer({ usecases, onAnalysisComplete, initialText, initialUsecase }: AnalyzerProps) {
  const { getToken } = useAuth()
  const [text, setText] = useState('')
  const [selectedUsecase, setSelectedUsecase] = useState(usecases[0]?.id || '')
  const [searchQuery, setSearchQuery] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isParsing, setIsParsing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (initialText !== undefined) {
      setText(initialText)
    }
    if (initialUsecase !== undefined) {
      setSelectedUsecase(initialUsecase)
    }
  }, [initialText, initialUsecase])

  const selectedUsecaseData = usecases.find(uc => uc.id === selectedUsecase)

  const filteredUsecases = usecases.filter(uc =>
    uc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    uc.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const validation = validateFile(file)
    if (!validation.valid) {
      setError(validation.error || 'Invalid file type or size')
      return
    }

    try {
      setIsParsing(true)
      setError('')
      const result = await parseFile(file)
      setText(prev => prev ? `${prev}\n\n${result.text}` : result.text)
    } catch (err: any) {
      setError(err.message || 'Failed to parse file')
    } finally {
      setIsParsing(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleAnalyze = async () => {
    if (!text.trim() || !selectedUsecase) return

    try {
      setLoading(true)
      setError('')
      setResult('')

      const token = await getToken()
      if (!token) throw new Error('Not authenticated')

      const response = await api.analyze({
        text,
        usecase_id: selectedUsecase,
      }, token)

      setResult(response.result)
      onAnalysisComplete()
    } catch (err: any) {
      setError(err.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setResult('')
    setError('')
  }

  const getUsecaseIcon = (name: string) => {
    if (name.includes('Blog')) return '🛡️'
    if (name.includes('Email')) return '🤍'
    if (name.includes('Bridge')) return '💜'
    if (name.includes('Phrase')) return '💜'
    return '✨'
  }

  return (
    <div className="analyzer-container">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>Content Generation</h2>
          <p>Select a role and provide your input to generate AI-powered content.</p>
        </div>

        <div className="roles-section">
          <div className="roles-header">
            <span className="roles-icon">🛡️</span>
            <h3>Select Role</h3>
          </div>

          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search roles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="roles-list">
            {filteredUsecases.map(uc => (
              <div
                key={uc.id}
                className={`role-card ${selectedUsecase === uc.id ? 'active' : ''}`}
                onClick={() => setSelectedUsecase(uc.id)}
              >
                <div className="role-card-header">
                  <h4>{uc.name}</h4>
                  <span className="role-icon">{getUsecaseIcon(uc.name)}</span>
                </div>
                <p>{uc.description}</p>
                {selectedUsecase === uc.id && <div className="active-indicator">✓</div>}
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <div className="input-section">
          <div className="section-label">
            <span className="icon">✍️</span>
            <h3>Input</h3>
          </div>
          <div className="using-role">
            Using: <span>{selectedUsecaseData?.name || 'Select a role'}</span>
          </div>

          <div className="textarea-wrapper">
            <textarea
              placeholder="Enter your request here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={isParsing || loading}
            />

            <input
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              accept=".pdf,.doc,.docx,.txt"
              onChange={handleFileUpload}
            />

            <button
              className="upload-btn"
              onClick={() => fileInputRef.current?.click()}
              title="Upload PDF, Word, or TXT file"
              disabled={isParsing || loading}
            >
              {isParsing ? '⏳' : '➕'}
            </button>

            <div className="char-count">{text.length} characters</div>
          </div>

          <button
            className="generate-btn"
            onClick={handleAnalyze}
            disabled={loading || !text.trim()}
          >
            {loading ? 'Generating...' : '✨ Generate Content'}
          </button>

          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="output-section">
          <div className="output-header">
            <div className="output-title">
              <span className="icon">📄</span>
              <h3>Output</h3>
              {result && <span className="output-chars">{result.length} chars</span>}
            </div>
            <div className="output-actions">
              <button
                className="action-btn"
                onClick={() => navigator.clipboard.writeText(result)}
                disabled={!result}
              >
                📋 Copy
              </button>
              <button
                className="action-btn btn-clear"
                onClick={handleClear}
                disabled={!text && !result}
              >
                ✕ Clear
              </button>
            </div>
          </div>

          <div className="output-content">
            {loading ? (
              <div className="loading-state">Processing...</div>
            ) : result ? (
              <div className="result-text">{result}</div>
            ) : (
              <div className="empty-state">Generated content will appear here</div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
