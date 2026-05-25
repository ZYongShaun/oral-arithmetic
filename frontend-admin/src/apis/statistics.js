import request from '@/utils/request'

export function getTodayStats() {
  return request.get('/api/v1/statistics/today')
}

export function getLeaderboard(params) {
  return request.get('/api/v1/statistics/leaderboard', { params })
}

export function getUserHistory(userId, days = 30) {
  return request.get(`/api/v1/statistics/user/${userId}/history`, { params: { days } })
}

export function exportLeaderboard(period) {
  return request.get('/api/v1/statistics/leaderboard/export', { 
    params: { period },
    responseType: 'blob'
  })
}
