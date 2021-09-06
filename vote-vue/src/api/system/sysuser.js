import request from '@/utils/request'

// 查询用户列表
export function userList(data) {
  return request({
    url: '/api/system/user/get-user-list',
    method: 'get',
    params: data
  })
}

// 查询用户详细
export function getUser(data) {
  return request({
    url: '/api/system/user/get-user-info',
    method: 'get',
    params: data
  })
}

// 保存用户
export function saveUser(data) {
  return request({
    url: '/api/system/user/save-user',
    method: 'post',
    data: data
  })
}

// 删除用户
export function delUser(data) {
  return request({
    url: '/api/system/user/del-user',
    method: 'get',
    params: data
  })
}

// 验证登录名
export function checkLoginName(data) {
  return request({
    url: '/api/system/user/check-login-name',
    method: 'get',
    params: data
  })
}

// 用户密码重置
export function resetUserPwd(data) {
  return request({
    url: '/api/system/user/rest-password',
    method: 'get',
    params: data
  })
}

// 用户头像上传
export function uploadAvatar(data) {
  return request({
    url: '/api/v1/user/avatar',
    method: 'post',
    data: data
  })
}

