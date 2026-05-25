import request from '@/utils/request'

// Get list of wrong questions for a child (query param child_id)
export function getWrongQuestions(childId, params = {}) {
  return request({
    url: '/wrong-questions/',
    method: 'get',
    params: { child_id: childId, ...params }
  })
}

// Delete a specific wrong question record (by wrong_question_id, not questionId)
export function deleteWrongQuestion(wrongQuestionId) {
  return request({
    url: `/wrong-questions/${wrongQuestionId}`,
    method: 'delete'
  })
}

// Mark a wrong question as mastered (review endpoint)
export function markMastered(childId, questionId) {
  return request({
    url: '/wrong-questions/review',
    method: 'post',
    data: { child_id: childId, question_id: questionId }
  })
}

// Get stats for wrong questions (query param child_id)
export function getStats(childId) {
  return request({
    url: '/wrong-questions/stats',
    method: 'get',
    params: { child_id: childId }
  })
}

// Alias for Home.vue
export function getWrongQuestionsStats(childId) {
  return getStats(childId)
}
