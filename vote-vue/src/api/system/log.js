import request from '@/utils/request'

// 查询登录日志列表
export function loginList(query) {
  return request({
    url: '/api/system/log/login-log',
    method: 'get',
    params: query
  })
}

// 查询操作日志列表
export function opeList(query) {
  return request({
    url: '/api/system/log/operate-log',
    method: 'get',
    params: query
  })
}
