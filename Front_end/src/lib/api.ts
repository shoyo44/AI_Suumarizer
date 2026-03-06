const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface Usecase {
  id: string
  name: string
  description: string
  output_format: string
  category: string
  extra_params: string[]
}

export interface AnalyzeRequest {
  text: string
  usecase_id: string
  target_language?: string
}

export interface AnalyzeResponse {
  usecase_id: string
  usecase_name: string
  result: string
  user_email?: string
  history_id?: string
}

export interface HistoryItem {
  id: string
  usecase_id: string
  usecase_name: string
  input_preview: string
  input_text: string
  result: string
  created_at: string
  is_public?: boolean
  share_id?: string
}

export interface UserInfo {
  uid: string
  email?: string
  name?: string
  picture?: string
  total_analyses: number
}

export interface WeeklyUsage {
  week: string
  count: number
}

export interface TopUsecase {
  name: string
  count: number
}

export interface CategoryBreakdown {
  category: string
  count: number
}

export interface AnalyticsData {
  weekly_usage: WeeklyUsage[]
  total_words: number
  avg_words_per_analysis: number
  top_usecases: TopUsecase[]
  category_breakdown: CategoryBreakdown[]
  streak_days: number
  total_analyses: number
}

class ApiClient {
  private getHeaders(token?: string) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return headers
  }

  async getUsecases(): Promise<Usecase[]> {
    const response = await fetch(`${API_BASE_URL}/usecases`)
    if (!response.ok) throw new Error('Failed to fetch usecases')
    return response.json()
  }

  async getCurrentUser(token: string): Promise<UserInfo> {
    const response = await fetch(`${API_BASE_URL}/me`, {
      headers: this.getHeaders(token),
    })
    if (!response.ok) throw new Error('Failed to fetch user info')
    return response.json()
  }

  async analyze(request: AnalyzeRequest, token: string): Promise<AnalyzeResponse> {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: this.getHeaders(token),
      body: JSON.stringify(request),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Analysis failed')
    }
    return response.json()
  }

  async getHistory(token: string, limit = 20, skip = 0): Promise<HistoryItem[]> {
    const response = await fetch(
      `${API_BASE_URL}/history?limit=${limit}&skip=${skip}`,
      {
        headers: this.getHeaders(token),
      }
    )
    if (!response.ok) throw new Error('Failed to fetch history')
    return response.json()
  }

  async getAnalytics(token: string): Promise<AnalyticsData> {
    const response = await fetch(`${API_BASE_URL}/analytics`, {
      headers: this.getHeaders(token),
    })
    if (!response.ok) throw new Error('Failed to fetch analytics')
    return response.json()
  }

  async deleteHistoryItem(historyId: string, token: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/history/${historyId}`, {
      method: 'DELETE',
      headers: this.getHeaders(token),
    })
    if (!response.ok) throw new Error('Failed to delete history item')
  }

  async shareHistoryItem(historyId: string, token: string): Promise<{ share_id: string }> {
    const response = await fetch(`${API_BASE_URL}/history/${historyId}/share`, {
      method: 'POST',
      headers: this.getHeaders(token),
    })
    if (!response.ok) throw new Error('Failed to share item')
    return response.json()
  }

  async getSharedItem(shareId: string): Promise<HistoryItem> {
    const response = await fetch(`${API_BASE_URL}/shared/${shareId}`)
    if (!response.ok) throw new Error('Shared item not found')
    return response.json()
  }
}

export const api = new ApiClient()
