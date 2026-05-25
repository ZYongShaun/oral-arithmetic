import request from '@/utils/request'

export function getBalance(childId) {
  return request({
    url: `/stars/balance/${childId}`,
    method: 'get'
  })
}

export function getTransactions(childId, params) {
  return request({
    url: `/stars/transactions/${childId}`,
    method: 'get',
    params
  })
}

export function getStarTransactions(childId, params) {
  return getTransactions(childId, params)
}

export function getShop() {
  return request({
    url: '/stars/shop',
    method: 'get'
  })
}

// Use spend endpoint for purchasing items
export function purchase(childId, data) {
  return request({
    url: '/stars/spend',
    method: 'post',
    data: { child_id: childId, ...data }
  })
}

export const getStarBalance = getBalance
export const getShopItems = getShop
export const purchaseShopItem = purchase
