import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/api/system/auth/login',
    method: 'post',
    data
  })
}

// 登出
export function logout() {
  return request({
    url: '/api/system/auth/login-out',
    method: 'get'
  })
}

// 获取用户详情
export function getUserInfo(data) {
  return request({
    url: '/api/system/auth/get-user-info',
    method: 'post',
    data
  })
}
