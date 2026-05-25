import request from '@/utils/request'

export const questionsAPI = {
  getRandom(data) {
    return request.post('/questions/random', data)
  },
  getQuestions(params) {
    return request.get('/questions', { params })
  },
  createQuestion(data) {
    return request.post('/questions', data)
  },
  updateQuestion(questionId, data) {
    return request.put(`/questions/${questionId}`, data)
  },
  deleteQuestion(questionId) {
    return request.delete(`/questions/${questionId}`)
  }
}
