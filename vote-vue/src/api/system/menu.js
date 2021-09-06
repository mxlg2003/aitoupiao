import request from '@/utils/request'

// 查询菜单列表
export function getMenuList(data) {
  return request({
    url: '/api/system/menu/get-menu-list',
    method: 'get',
    params: data
  })
}

// 查询菜单详情
export function getMenu(data) {
  return request({
    url: '/api/system/menu/get-menu-info',
    method: 'get',
    params: data
  })
}

// 新增菜单
export function saveMenu(data) {
  return request({
    url: '/api/system/menu/save-menu',
    method: 'post',
    data: data
  })
}

// 删除菜单
export function delMenu(data) {
  return request({
    url: '/api/system/menu/del-menu',
    method: 'get',
    params: data
  })
}
