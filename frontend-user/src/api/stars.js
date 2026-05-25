import request from '@/utils/request'

export const getStarBalance = (childId) => {
  return request.get(`/stars/balance/${childId}`)
}

export const getStarTransactions = (childId, params = {}) => {
  return request.get(`/stars/transactions/${childId}`, { params })
}

export const spendStars = (data) => {
  return request.post('/stars/spend', data)
}

export const getShopItems = () => {
  return request.get('/stars/shop')
}

export const purchaseShopItem = (itemId, data = {}) => {
  return request.post(`/stars/shop/${itemId}/purchase`, data)
}

export const starsAPI = {
  getBalance(childId) {
    return request.get(`/stars/balance/${childId}`)
  },
  getTransactions(childId, params) {
    return request.get(`/stars/transactions/${childId}`, { params })
  },
  spendStars(data) {
    return request.post('/stars/spend', data)
  },
  getShop() {
    return request.get('/stars/shop')
  }
}
