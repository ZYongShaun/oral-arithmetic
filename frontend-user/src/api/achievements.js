import request from '@/utils/request'

export const getAchievements = (childId) => {
  return request.get('/achievements', { params: { child_id: childId } })
}

export const achievementsAPI = {
  getAll() {
    return request.get('/achievements')
  },
  getProgress(childId) {
    return request.get(`/achievements/${childId}/progress`)
  }
}
