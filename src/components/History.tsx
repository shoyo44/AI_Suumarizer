import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../lib/api'
import type { HistoryItem } from '../lib/api'
import './History.css'

interface HistoryProps {
  history: HistoryItem[]
  onRefresh: () => void
  onReuse: (text: string, usecase: string) => void
}

export default function History({ history, onRefresh, onReuse }: HistoryProps) {
  const { getToken } = useAuth()
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this item?')) return

    try {
      setDeleting(id)
      const token = await getToken()
      if (!token) throw new Error('Not authenticated')

      await api.deleteHistoryItem(id, token)
      onRefresh()
      if (selectedItem?.id === id) {
        setSelectedItem(null)
      }
    } catch (error) {
      console.error('Failed to delete:', error)
      alert('Failed to delete item')
    } finally {
      setDeleting(null)
    }
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }

  if (history.length === 0) {
    return (
      <div className="history-empty">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="12" cy="12" r="10" />
          <polyline points="12 6 12 12 16 14" />
        </svg>
        <h3>No History Yet</h3>
        <p>Your analysis history will appear here once you start analyzing text.</p>
      </div>
    )
  }

  return (
    <div className="history">
      <div className="history-grid">
        <div className="history-list">
          <div className="list-header">
            <h2>Recent Analyses</h2>
            <span className="count-badge">{history.length} items</span>
          </div>

          <div className="list-items">
            {history.map((item) => (
              <div
                key={item.id}
                className={`history-item ${selectedItem?.id === item.id ? 'active' : ''}`}
                onClick={() => setSelectedItem(item)}
              >
                <div className="item-header">
                  <span className="item-usecase">{item.usecase_name}</span>
                  <button
                    className="delete-btn"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDelete(item.id)
                    }}
                    disabled={deleting === item.id}
                  >
                    {deleting === item.id ? (
                      <div className="btn-spinner-small"></div>
                    ) : (
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                      </svg>
                    )}
                  </button>
                </div>
                <p className="item-preview">{item.input_preview}</p>
                <span className="item-date">{formatDate(item.created_at)}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="history-detail">
          {selectedItem ? (
            <>
              <div className="detail-header">
                <div>
                  <h3>{selectedItem.usecase_name}</h3>
                  <span className="detail-date">{formatDate(selectedItem.created_at)}</span>
                </div>
                <div className="header-actions">
                  <button
                    className="reuse-btn"
                    onClick={() => onReuse(selectedItem.input_text || selectedItem.input_preview, selectedItem.usecase_id)}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <polyline points="9 21 3 21 3 15"></polyline>
                      <line x1="21" y1="3" x2="14" y2="10"></line>
                      <line x1="3" y1="21" x2="10" y2="14"></line>
                    </svg>
                    Reuse Prompt
                  </button>
                  <button
                    className="copy-btn"
                    onClick={() => navigator.clipboard.writeText(selectedItem.result)}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                    </svg>
                    Copy Result
                  </button>
                </div>
              </div>

              <div className="detail-section">
                <h4>Input</h4>
                <div className="detail-content">{selectedItem.input_text || selectedItem.input_preview}</div>
              </div>

              <div className="detail-section">
                <h4>Result</h4>
                <div className="detail-content">{selectedItem.result}</div>
              </div>
            </>
          ) : (
            <div className="detail-placeholder">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <p>Select an item to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
