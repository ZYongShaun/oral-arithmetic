import { defineStore } from 'pinia'
import { getStarBalance, getStarTransactions } from '@/api/stars'
import { getAchievements } from '@/api/achievements'
import { getStreakInfo } from '@/api/streaks'
import { getDailyTaskStatus } from '@/api/dailyTasks'

export const useGameStore = defineStore('game', {
  state: () => ({
    stars: 0,
    achievements: [],
    streak: {
      currentStreak: 0,
      shields: 0,
      longestStreak: 0
    },
    dailyTask: {
      todayCount: 0,
      completed: false,
      rewardClaimed: false
    },
    transactions: [],
    loading: false
  }),
  
  getters: {
    totalStars: (state) => state.stars,
    unlockedAchievements: (state) => state.achievements.filter(a => a.unlocked),
    lockedAchievements: (state) => state.achievements.filter(a => !a.unlocked),
    achievementProgress: (state) => {
      const total = state.achievements.length
      const unlocked = state.unlockedAchievements.length
      return total === 0 ? 0 : Math.round((unlocked / total) * 100)
    }
  },
  
  actions: {
    async loadGameData(childId) {
      if (!childId) return
      
      this.loading = true
      try {
        await Promise.all([
          this.loadStars(childId),
          this.loadAchievements(childId),
          this.loadStreak(childId),
          this.loadDailyTask(childId)
        ])
      } catch (error) {
        console.error('加载游戏数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadStars(childId) {
      try {
        const response = await getStarBalance(childId)
        if (response.data) {
          this.stars = response.data.balance || 0
        }
      } catch (error) {
        console.error('加载星星余额失败:', error)
      }
    },
    
    async loadTransactions(childId, params = {}) {
      try {
        const response = await getStarTransactions(childId, params)
        if (response.data) {
          this.transactions = response.data.items || []
          return {
            items: response.data.items || [],
            total: response.data.total || 0
          }
        }
      } catch (error) {
        console.error('加载交易记录失败:', error)
        throw error
      }
    },
    
    async loadAchievements(childId) {
      try {
        const response = await getAchievements(childId)
        if (response.data || Array.isArray(response)) {
          const data = response.data || response
          this.achievements = data.map(item => ({
            id: item.id,
            title: item.title,
            description: item.description,
            type: item.type,
            unlocked: item.unlocked || false,
            current: item.current || 0,
            target: item.target || 0,
            stars: item.stars || 0,
            unlockedAt: item.unlocked_at
          }))
        }
      } catch (error) {
        console.error('加载成就失败:', error)
      }
    },
    
    async loadStreak(childId) {
      try {
        const response = await getStreakInfo(childId)
        if (response.data) {
          this.streak = {
            currentStreak: response.data.currentStreak || 0,
            shields: response.data.shields || 0,
            longestStreak: response.data.longestStreak || 0
          }
        }
      } catch (error) {
        console.error('加载连胜信息失败:', error)
      }
    },
    
    async loadDailyTask(childId) {
      try {
        const response = await getDailyTaskStatus(childId)
        if (response.data) {
          this.dailyTask = {
            todayCount: response.data.todayCount || 0,
            completed: response.data.completed || false,
            rewardClaimed: response.data.rewardClaimed || false
          }
        }
      } catch (error) {
        console.error('加载每日任务失败:', error)
      }
    },
    
    updateStars(amount) {
      this.stars = Math.max(0, this.stars + amount)
    },
    
    updateStreak(streakData) {
      this.streak = { ...this.streak, ...streakData }
    },
    
    updateDailyTask(taskData) {
      this.dailyTask = { ...this.dailyTask, ...taskData }
    },
    
    addTransaction(transaction) {
      this.transactions.unshift(transaction)
    },
    
    updateAchievement(achievementData) {
      const index = this.achievements.findIndex(a => a.id === achievementData.id)
      if (index !== -1) {
        this.achievements[index] = { ...this.achievements[index], ...achievementData }
      }
    }
  }
})
