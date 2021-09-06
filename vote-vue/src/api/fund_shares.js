import request from '@/utils/request'

// 基金列表
export function fundList(data) {
  return request({
    url: '/api/fund-shares/fund/list',
    method: 'post',
    data
  })
}

// 单个基金日期列表
export function fundDateList(data) {
  return request({
    url: '/api/fund-shares/fund/date-list',
    method: 'post',
    data
  })
}

// 单个基金日期列表
export function fundSharesList(data) {
  return request({
    url: '/api/fund-shares/fund/fund-shares-info',
    method: 'post',
    data
  })
}

// 股票列表
export function sharesList(data) {
  return request({
    url: '/api/fund-shares/shares/list',
    method: 'post',
    data
  })
}

// 股票日涨信息
export function sharesDateList(data) {
  return request({
    url: '/api/fund-shares/shares/date-list',
    method: 'post',
    data
  })
}

// 基金持股情况
export function sharesFundInfo(data) {
  return request({
    url: '/api/fund-shares/shares/shares-fund-list',
    method: 'post',
    data
  })
}

// 基金持股情况
export function getHoldHeavyweight(data) {
  return request({
    url: '/api/fund-shares/shares/heavyweight-shares-list',
    method: 'post',
    data
  })
}
