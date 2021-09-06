import request from '@/utils/request'

export function getDeptList(query) {
  return request({
    url: '/api/system/dept/get-dept-list',
    method: 'get',
    params: query
  })
}

// 查询部门详细
export function getDept(data) {
  return request({
    url: '/api/system/dept/get-dept-info',
    method: 'get',
    params: data
  })
}

// 修改部门
export function saveDept(data) {
  return request({
    url: '/api/system/dept/save-dept',
    method: 'post',
    data: data
  })
}

// 删除部门
export function delDept(data) {
  return request({
    url: '/api/system/dept/del-dept',
    method: 'get',
    params: data
  })
}
