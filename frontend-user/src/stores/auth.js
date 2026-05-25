import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || '{}'),
    currentChildId: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('access_token', token)
    },
    
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('user_info', JSON.stringify(userInfo))
    },
    
    setCurrentChildId(childId) {
      this.currentChildId = childId
      localStorage.setItem('current_child_id', childId)
    },
    
    logout() {
      this.token = ''
      this.userInfo = {}
      this.currentChildId = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      localStorage.removeItem('current_child_id')
      localStorage.removeItem('recent_user_ids')
    }
  }
})
