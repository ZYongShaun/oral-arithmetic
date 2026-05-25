import request from '@/utils/request'

// Current leaderboard (weekly/daily) - also used as getLeaderboard
export function getCurrent(params) {
  return request({
    url: '/leaderboards/current',
    method: 'get',
    params
  })
}

// Alias for Leaderboard.vue
export function getLeaderboard(childId, params = {}) {
  return getCurrent({ child_id: childId, ...params })
}

// Historical leaderboard (may need to implement endpoint)
export function getHistorical(params) {
  return request({
    url: '/leaderboards/historical',
    method: 'get',
    params
  })
}

// Get leaderboard groups (class/grade groups)
export function getGroups() {
  return request({
    url: '/leaderboards/groups',
    method: 'get'
  })
}
