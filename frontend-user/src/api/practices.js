import request from '@/utils/request'

export const practicesAPI = {
  startPractice(data) {
    return request.post('/practices/start', data)
  },
  submitPractice(data) {
    return request.post('/practices/submit', data)
  },
  getHistory(childId, params) {
    return request.get(`/practices/history?child_id=${childId}`, { params })
  },
  getPracticeDetail(practiceId) {
    return request.get(`/practices/${practiceId}`)
  }
}
