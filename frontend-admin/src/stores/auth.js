import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminAPI } from '@/apis/admin'

export const useAdminStore = defineStore('admin', () => {
  const token = ref(localStorage.getItem('admin_token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('admin_user') || '{}'))
  
  const isLoggedIn = computed(() => !!token.value)
  
  async function login(credentials) {
    try {
      const response = await adminAPI.login(credentials)
      token.value = response.access_token
      userInfo.value = response.user
      
      localStorage.setItem('admin_token', response.access_token)
      localStorage.setItem('admin_user', JSON.stringify(response.user))
      
      return { success: true, data: response }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || '登录失败' }
    }
  }
  
  function logout() {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }
  
  function clearAuth() {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    logout,
    clearAuth
  }
})
