import request from '@/utils/request'

// 查询角色列表
export function getRoleList(data) {
  return request({
    url: '/api/system/role/get-role-list',
    method: 'get',
    params: data
  })
}

// 查询角色详细
export function getRole(data) {
  return request({
    url: '/api/system/role/get-role-info',
    method: 'get',
    params: data,
  })
}

// 保存角色
export function saveRole(data) {
  return request({
    url: '/api/system/role/role-save',
    method: 'post',
    data: data
  })
}

// 删除角色
export function delRole(data) {
  return request({
    url: '/api/system/role/del-role',
    method: 'get',
    params: data
  })
}

export function getRoutes() {
  return request({
    url: '/api/system/auth/get-user-menu',
    method: 'get'
  })
}

