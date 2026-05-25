import request from '@/utils/request'

export function getRandomQuestions(data) {
  // data should match RandomQuestionsRequest: { grade_level, difficulty_level, count, question_types? }
  return request({
    url: '/questions/random',
    method: 'post',
    data
  })
}

export function submitPractice(data) {
  // data should be { practice_id, answers, time_spent }
  return request({
    url: '/practices/submit',
    method: 'post',
    data
  })
}

export function getHistory(params) {
  // params should include child_id, skip, limit
  return request({
    url: '/practices/history',
    method: 'get',
    params
  })
}

export function getDetail(id) {
  return request({
    url: `/practices/${id}`,
    method: 'get'
  })
}

export const getPracticeHistory = getHistory
