import request from '@/utils/request'

export const getStreakInfo = (childId) => {
  return request.get(`/streaks/${childId}`)
}

export const useShield = (childId, cost = 50) => {
  return request.post(`/streaks/${childId}/use-shield`, { cost })
}

export const getMilestones = (childId) => {
  return request.get(`/streaks/${childId}/milestones`)
}

export const streaksAPI = {
  getStreak(childId) {
    return request.get(`/streaks/${childId}`)
  },
  useShield(childId) {
    return request.post(`/streaks/${childId}/use-shield`)
  },
  getMilestones(childId) {
    return request.get(`/streaks/${childId}/milestones`)
  }
}
