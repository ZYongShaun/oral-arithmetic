import request from '@/utils/request'

export function getProfile() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export function updateProfile(data) {
  return request({
    url: '/users/me',
    method: 'put',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/users/change-password',
    method: 'post',
    data
  })
}
