import request from '@/utils/request'

export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

export function getProfile() {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

export function updateProfile(data) {
  return request({
    url: '/users/profile',
    method: 'put',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/users/password/change',
    method: 'post',
    data
  })
}

export function quickLogin(data) {
  return request({
    url: '/auth/quick-login',
    method: 'post',
    data
  })
}

export function getRecentUsers(params) {
  return request({
    url: '/auth/recent',
    method: 'get',
    params
  })
}

export const authAPI = {
  register,
  login,
  logout,
  getProfile,
  updateProfile,
  changePassword,
  quickLogin,
  getRecentUsers
}

export const getUserProfile = getProfile
export const updateUserProfile = updateProfile
