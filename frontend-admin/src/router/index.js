import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'UserList',
    component: () => import('@/views/UserList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: () => import('@/views/UserDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/questions',
    name: 'QuestionList',
    component: () => import('@/views/QuestionList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/questions/create',
    name: 'QuestionCreate',
    component: () => import('@/views/QuestionEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/questions/:id/edit',
    name: 'QuestionEdit',
    component: () => import('@/views/QuestionEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/rules',
    name: 'RuleConfig',
    component: () => import('@/views/RuleConfig.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/system',
    name: 'SystemConfig',
    component: () => import('@/views/SystemConfig.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/Statistics.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admins',
    name: 'AdminList',
    component: () => import('@/views/AdminList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/logs',
    name: 'OperationLogs',
    component: () => import('@/views/OperationLogs.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/achievements',
    name: 'AchievementManagement',
    component: () => import('@/views/AchievementManagement.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/leaderboards',
    name: 'LeaderboardManagement',
    component: () => import('@/views/LeaderboardManagement.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
