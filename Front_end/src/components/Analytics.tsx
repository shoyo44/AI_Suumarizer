import type { AnalyticsData } from '../lib/api'
import './Analytics.css'

interface AnalyticsProps {
    data: AnalyticsData | null
    total: number
    onExit: () => void
}

const CATEGORY_ICONS: Record<string, string> = {
    extraction: '📋',
    analysis: '🔬',
    summarization: '📝',
    simplification: '💡',
    education: '🎓',
    critical_thinking: '🧐',
    visualization: '🧠',
    business: '📈',
    creative: '🎨',
    other: '📦',
}

export default function Analytics({ data, total, onExit }: AnalyticsProps) {
    const weeklyUsage = data?.weekly_usage || []
    const topUsecases = data?.top_usecases || []
    const categories = data?.category_breakdown || []
    const totalWords = data?.total_words || 0
    const avgWords = data?.avg_words_per_analysis || 0
    const streak = data?.streak_days || 0
    const totalAnalyses = data?.total_analyses || total

    const maxCount = Math.max(...weeklyUsage.map(d => d.count), 1)
    const maxUcCount = Math.max(...topUsecases.map(u => u.count), 1)
    const maxCatCount = Math.max(...categories.map(c => c.count), 1)

    // Derive avg per week
    const avgPerWeek = weeklyUsage.length > 0
        ? (weeklyUsage.reduce((s, d) => s + d.count, 0) / weeklyUsage.length).toFixed(1)
        : '0'

    return (
        <div className="analytics-page">
            {/* Header */}
            <div className="analytics-header">
                <div>
                    <h2 className="analytics-title">Usage Analytics</h2>
                    <p className="analytics-subtitle">Your AI content generation insights — last 12 weeks</p>
                </div>
                <button className="analytics-exit-btn" onClick={onExit}>
                    ← Back to Analyzer
                </button>
            </div>

            {/* Stat Cards Row */}
            <div className="stat-cards-row">
                <div className="stat-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-info">
                        <span className="stat-value">{totalAnalyses}</span>
                        <span className="stat-label">Total Analyses</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">📝</div>
                    <div className="stat-info">
                        <span className="stat-value">{totalWords.toLocaleString()}</span>
                        <span className="stat-label">Words Processed</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">📐</div>
                    <div className="stat-info">
                        <span className="stat-value">{avgWords.toLocaleString()}</span>
                        <span className="stat-label">Avg Words / Analysis</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">🔥</div>
                    <div className="stat-info">
                        <span className="stat-value">{streak}</span>
                        <span className="stat-label">Day Streak</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">⚡</div>
                    <div className="stat-info">
                        <span className="stat-value">{avgPerWeek}</span>
                        <span className="stat-label">Avg / Week</span>
                    </div>
                </div>
            </div>

            {/* Charts Grid */}
            <div className="analytics-grid">
                {/* Weekly Activity Chart */}
                <div className="analytics-card chart-wide">
                    <h3 className="card-title">📈 Weekly Activity — Last 12 Weeks</h3>
                    <div className="bar-chart">
                        {weeklyUsage.length === 0 && (
                            <p className="chart-empty">No activity data yet. Start generating content!</p>
                        )}
                        {weeklyUsage.map(d => (
                            <div key={d.week} className="bar-col">
                                <div className="bar-tooltip">{d.count}</div>
                                <div
                                    className="bar-fill"
                                    style={{ height: `${(d.count / maxCount) * 100}%` }}
                                ></div>
                                <span className="bar-label">{d.week.replace(/^\d{4}-/, '')}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Top Usecases */}
                <div className="analytics-card">
                    <h3 className="card-title">🏆 Most Used Roles</h3>
                    {topUsecases.length === 0 && (
                        <p className="chart-empty">No role usage data yet.</p>
                    )}
                    <div className="top-usecases-list">
                        {topUsecases.map((uc, i) => (
                            <div key={uc.name} className="top-usecase-item">
                                <div className="top-usecase-rank">#{i + 1}</div>
                                <div className="top-usecase-info">
                                    <span className="top-usecase-name">{uc.name}</span>
                                    <div className="top-usecase-bar-bg">
                                        <div
                                            className="top-usecase-bar-fill"
                                            style={{ width: `${(uc.count / maxUcCount) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                                <span className="top-usecase-count">{uc.count}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Category Breakdown */}
                <div className="analytics-card">
                    <h3 className="card-title">🗂️ Category Breakdown</h3>
                    {categories.length === 0 && (
                        <p className="chart-empty">No category data yet.</p>
                    )}
                    <div className="category-list">
                        {categories.map(cat => (
                            <div key={cat.category} className="category-item">
                                <div className="category-icon">{CATEGORY_ICONS[cat.category] || '📦'}</div>
                                <div className="category-info">
                                    <div className="category-name-row">
                                        <span className="category-name">{cat.category.replace('_', ' ')}</span>
                                        <span className="category-count">{cat.count}</span>
                                    </div>
                                    <div className="category-bar-bg">
                                        <div
                                            className="category-bar-fill"
                                            style={{ width: `${(cat.count / maxCatCount) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Streak & Insight */}
                    <div className="insight-box" style={{ marginTop: '1.5rem' }}>
                        <div className="insight-label">💡 Quick Insight</div>
                        <p className="insight-text">
                            {streak >= 3
                                ? `Amazing! You're on a ${streak}-day streak. Keep the momentum going!`
                                : totalAnalyses > 20
                                    ? 'You\'re a power user! Keep exploring different analysis roles.'
                                    : totalAnalyses > 5
                                        ? 'Great progress! Try different roles to unlock new insights.'
                                        : 'Welcome aboard! Start exploring our 19 AI-powered roles.'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
