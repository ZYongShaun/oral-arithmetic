import request from '@/utils/request'

export const childrenAPI = {
  getChildren(params) {
    return request.get('/children', { params })
  },
  createChild(data) {
    return request.post('/children', data)
  },
  getChild(childId) {
    return request.get(`/children/${childId}`)
  },
  updateChild(childId, data) {
    return request.put(`/children/${childId}`, data)
  },
  deleteChild(childId) {
    return request.delete(`/children/${childId}`)
  }
}
