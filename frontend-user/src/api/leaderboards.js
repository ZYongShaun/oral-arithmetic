import request from '@/utils/request'

export const getLeaderboard = (childId, params = {}) => {
  return request.get('/leaderboards', { params: { child_id: childId, ...params } })
}

export const getGroupInfo = (childId) => {
  return request.get(`/leaderboards/groups`, { params: { child_id: childId } })
}

export const getGroupLeaderboard = (groupId) => {
  return request.get(`/leaderboards/groups/${groupId}`)
}

export const leaderboardsAPI = {
  getCurrent(childId) {
    return request.get(`/leaderboards/current?child_id=${childId}`)
  },
  getGroupInfo(childId) {
    return request.get(`/leaderboards/groups?child_id=${childId}`)
  }
}
