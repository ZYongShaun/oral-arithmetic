import request from '@/utils/request'

export function getChildren() {
  return request({
    url: '/children/',
    method: 'get'
  })
}

export function createChild(data) {
  return request({
    url: '/children/',
    method: 'post',
    data
  })
}

export function getChild(id) {
  return request({
    url: `/children/${id}`,
    method: 'get'
  })
}

export function updateChild(id, data) {
  return request({
    url: `/children/${id}`,
    method: 'put',
    data
  })
}

export function deleteChild(id) {
  return request({
    url: `/children/${id}`,
    method: 'delete'
  })
}
