import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../lib/api'
import type { Usecase, UserInfo, HistoryItem } from '../lib/api'
import Analyzer from './Analyzer'
import History from './History'
import './Dashboard.css'

export default function Dashboard() {
  const { user, signOut, getToken } = useAuth()
  const [usecases, setUsecases] = useState<Usecase[]>([])
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'analyzer' | 'history'>('analyzer')
  const [reuseData, setReuseData] = useState<{ text: string; usecase: string } | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    if (activeTab === 'history') {
      refreshHistory()
    }
  }, [activeTab])

  const loadData = async () => {
    try {
      setLoading(true)
      const [usecasesData, token] = await Promise.all([
        api.getUsecases(),
        getToken()
      ])

      setUsecases(usecasesData)

      if (token) {
        const [userInfoData, historyData] = await Promise.all([
          api.getCurrentUser(token),
          api.getHistory(token)
        ])
        setUserInfo(userInfoData)
        setHistory(historyData)
      }
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshHistory = async () => {
    const token = await getToken()
    if (token) {
      const historyData = await api.getHistory(token)
      setHistory(historyData)
      const userInfoData = await api.getCurrentUser(token)
      setUserInfo(userInfoData)
    }
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="app-layout">
      <header className="top-navbar">
        <div className="nav-left">
          <div className="nav-logo">
            {activeTab === 'history' ? (
              <button className="back-btn" onClick={() => setActiveTab('analyzer')} title="Back to Analyzer">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="19" y1="12" x2="5" y2="12"></line>
                  <polyline points="12 19 5 12 12 5"></polyline>
                </svg>
              </button>
            ) : (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="4" width="20" height="16" rx="2" stroke="white" strokeWidth="2" />
                <path d="M6 16L10 8L14 16L18 8" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            )}
          </div>
          <h1>{activeTab === 'history' ? 'History' : 'AI Summarizer'}</h1>
        </div>

        <div className="nav-right">
          <button
            className={`nav-icon-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'history' ? 'analyzer' : 'history')}
            title="View History"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          </button>
          <div className="user-profile">
            <div className="avatar">{user?.email?.charAt(0).toUpperCase() || 'U'}</div>
            <span className="user-name">{user?.displayName || user?.email?.split('@')[0] || 'User'}</span>
            <button className="menu-btn" onClick={signOut}>⋮</button>
          </div>
        </div>
      </header>

      <main className="main-container">
        {activeTab === 'analyzer' ? (
          <Analyzer
            usecases={usecases}
            onAnalysisComplete={refreshHistory}
            initialText={reuseData?.text}
            initialUsecase={reuseData?.usecase}
          />
        ) : (
          <History
            history={history}
            onRefresh={refreshHistory}
            onReuse={(text, usecase) => {
              setReuseData({ text, usecase })
              setActiveTab('analyzer')
            }}
          />
        )}
      </main>
    </div>
  )
}

