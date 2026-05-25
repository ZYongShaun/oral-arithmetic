import request from '@/utils/request'

export const getDailyTaskStatus = (childId, targetDate) => {
  const params = targetDate ? { date: targetDate } : {}
  return request.get(`/daily-tasks/${childId}`, { params })
}

export const claimDailyTaskReward = (childId, date) => {
  return request.post('/daily-tasks/claim', { child_id: childId, date })
}

export const dailyTasksAPI = {
  getStatus(childId, targetDate) {
    const params = targetDate ? { date: targetDate } : {}
    return request.get(`/daily-tasks/${childId}`, { params })
  },
  claimReward(childId, date) {
    return request.post('/daily-tasks/claim', { child_id: childId, date })
  }
}
