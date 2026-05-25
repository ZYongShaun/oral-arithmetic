import request from '@/utils/request'

export function getInfo(childId) {
  return request({
    url: `/streaks/${childId}`,
    method: 'get'
  })
}

export function getStreakInfo(childId) {
  return getInfo(childId)
}

// There's no buyShield endpoint directly. Possibly use /streaks/check to purchase shield? Or maybe it's spend stars.
// We'll map buyShield to POST /streaks/check? Actually that might be for checking streak.
// For now, we can leave these as placeholders or map to /streaks/check if needed.
export function buyShield(childId) {
  // If shield purchase is part of check or separate, adjust accordingly
  return request({
    url: `/streaks/check`,
    method: 'post',
    data: { child_id: childId, action: 'buy_shield' }
  })
}

export function useShield(childId) {
  return request({
    url: `/streaks/use-shield`,
    method: 'post',
    data: { child_id: childId }
  })
}
