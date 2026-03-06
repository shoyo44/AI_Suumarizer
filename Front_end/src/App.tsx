import './App.css'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import SharedAnalysis from './components/SharedAnalysis'

function AppContent() {
  const path = window.location.pathname
  if (path.startsWith('/shared/')) {
    const shareId = path.split('/')[2]
    if (shareId) {
      return <SharedAnalysis shareId={shareId} />
    }
  }

  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return user ? <Dashboard /> : <Login />
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
