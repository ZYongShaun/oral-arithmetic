import request from '@/utils/request'

// Get child's achievement progress
export function getChildAchievements(childId) {
  return request({
    url: `/achievements/${childId}/progress`,
    method: 'get'
  })
}

// Get list of all achievements (for display)
export function listAchievements() {
  return request({
    url: '/achievements/',
    method: 'get'
  })
}

export const getAchievements = listAchievements
