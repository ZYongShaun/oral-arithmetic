import request from '@/utils/request'

export const authAPI = {
  register(data) {
    return request.post('/auth/register', data)
  },
  login(data) {
    return request.post('/auth/login', data)
  },
  logout() {
    return request.post('/auth/logout')
  },
  getProfile() {
    return request.get('/auth/me')
  }
}
