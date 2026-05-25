import request from '@/utils/request'

export const wrongQuestionsAPI = {
  getWrongQuestions(childId, reviewed, params) {
    return request.get(`/wrong-questions?child_id=${childId}&reviewed=${reviewed}`, { params })
  },
  reviewWrongQuestion(wrongQuestionId) {
    return request.post(`/wrong-questions/review?wrong_question_id=${wrongQuestionId}`)
  },
  deleteWrongQuestion(wrongQuestionId) {
    return request.delete(`/wrong-questions/${wrongQuestionId}`)
  },
  getStats(childId) {
    return request.get(`/wrong-questions/stats?child_id=${childId}`)
  }
}
