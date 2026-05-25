import request from '@/utils/request'

export function getStatus(childId) {
  return request({
    url: `/daily-tasks/${childId}`,
    method: 'get'
  })
}

export function getDailyTaskStatus(childId) {
  return getStatus(childId)
}

export function claimReward(childId) {
  return request({
    url: `/daily-tasks/${childId}/claim`,
    method: 'post'
  })
}

export const claimDailyTaskReward = claimReward
