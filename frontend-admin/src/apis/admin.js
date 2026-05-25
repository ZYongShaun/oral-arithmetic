import request from '@/utils/request'

export const adminAPI = {
  // 管理员认证
  login(credentials) {
    return request.post('/api/admin/login', credentials)
  },
  logout() {
    return request.post('/api/admin/logout')
  },
  
  // 控制台
  getDashboard() {
    return request.get('/api/admin/dashboard')
  },
  
  // 统计数据 (新)
  getTodayStats() {
    return request.get('/api/v1/statistics/today')
  },
  getLeaderboard(params) {
    return request.get('/api/v1/statistics/leaderboard', { params })
  },
  exportLeaderboard(period) {
    return request.get(`/api/v1/statistics/leaderboard/export`, { 
      params: { period },
      responseType: 'blob' 
    })
  },
  getUserHistory(userId, days = 30) {
    return request.get(`/api/v1/statistics/user/${userId}/history`, { 
      params: { days } 
    })
  },
  
  // 用户管理 (家长用户)
  getParentUsers(params) {
    return request.get('/api/v1/admin/users', { params })
  },
  getParentUserDetail(userId) {
    return request.get(`/api/v1/admin/users/${userId}`)
  },
  updateParentUserStatus(userId, status) {
    return request.put(`/api/v1/admin/users/${userId}/status`, { status })
  },
  exportParentUsers() {
    return request.get('/api/v1/admin/users/export', { responseType: 'blob' })
  },
  
  // 原有的用户管理（孩子）保留但调整路径为 /admin/children
  getChildren(params) {
    return request.get('/api/admin/children', { params })
  },
  getChildDetail(childId) {
    return request.get(`/api/admin/children/${childId}`)
  },
  updateChildStatus(childId, status) {
    return request.put(`/api/admin/children/${childId}/status`, { status })
  },
  exportChildren() {
    return request.get('/api/admin/children/export', { responseType: 'blob' })
  },
  
  // 题目管理
  getQuestions(params) {
    return request.get('/api/admin/questions', { params })
  },
  createQuestion(data) {
    return request.post('/api/admin/questions', data)
  },
  updateQuestion(questionId, data) {
    return request.put(`/api/admin/questions/${questionId}`, data)
  },
  deleteQuestion(questionId) {
    return request.delete(`/api/admin/questions/${questionId}`)
  },
  batchImportQuestions(formData) {
    return request.post('/api/admin/questions/batch-import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // 出题规则
  getRules() {
    return request.get('/api/admin/questions/rules')
  },
  updateRules(rules) {
    return request.put('/api/admin/questions/rules', rules)
  },
  
  // 系统配置
  getConfigs() {
    return request.get('/api/admin/configs')
  },
  updateConfigs(configs) {
    return request.put('/api/admin/configs', configs)
  },
  
  // 数据统计 (旧的，可选保留)
  getStatistics(type, params = {}) {
    return request.get(`/api/admin/statistics/${type}`, { params })
  },
  exportStatistics(type) {
    return request.get(`/api/admin/statistics/${type}/export`, { responseType: 'blob' })
  },
  
  // 管理员管理
  getAdmins() {
    return request.get('/api/admin/admins')
  },
  createAdmin(data) {
    return request.post('/api/admin/admins', data)
  },
  deleteAdmin(adminId) {
    return request.delete(`/api/admin/admins/${adminId}`)
  },
  
  // 操作日志
  getOperationLogs(params) {
    return request.get('/api/admin/logs', { params })
  }
}
