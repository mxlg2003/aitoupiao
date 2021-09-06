import { asyncRoutes, constantRoutes } from '@/router'
import { getRoutes } from '@/api/system/role'
import Layout from '@/layout'

/**
 * 使用路由确定当前用户是否有权限
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * 使用权限标识判断当前用户是否具有权限
 */
function hasPathPermission(paths, route) {
  if (route.path) {
    return paths.some(path => route.path === path.path)
  } else {
    return true
  }
}

/**
  * 后台查询的菜单数据拼装成路由格式的数据
  */
export function generaMenu(routes, data) {
  data.forEach(item => {
    if (item.menu_type !== 2) {
      // 如果是外链，就不往children当中追加
      if (item.menu_type !== 3) {
        const menu = {
          path: item.menu_url,
          component: item.menu_code === 'Layout' ? Layout : loadView(item.menu_code),
          children: [],
          hidden: item.menu_type === 3,
          name: item.menu_name,
          meta: {
            title: item.menu_name,
            icon: item.menu_icon,
            noCache: true
          }
        }
        if (item.children) {
          generaMenu(menu.children, item.children)
        }
        routes.push(menu)
      }
      // 追加外链信息
      if (item.children) {
        item.children.forEach(child => {
          if (child.menu_type === 3) {
            routes.push({
              path: child.menu_url,
              component: child.menu_code === 'Layout' ? Layout : loadView(child.menu_code),
              hidden: true,
              name: child.menu_name,
              meta: {
                title: child.menu_name,
                icon: child.menu_icon,
                noCache: true
              }
            })
          }
        })
      }
    }
  })
}

export const loadView = (view) => { // 路由懒加载
  return (resolve) => require(['@/views' + view], resolve)
}

/**
 * 递归过滤异步路由列表
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

/**
 * 递归过滤异步路由列表
 */
export function filterAsyncPathRoutes(routes, paths) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPathPermission(paths, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncPathRoutes(tmp.children, paths)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      const loadMenuData = []

      getRoutes().then(response => {
        if (response.code !== 200) {
          this.$message({
            message: '菜单数据加载异常',
            type: 0
          })
        } else {
          Object.assign(loadMenuData, response.tree_menu_list)
          generaMenu(asyncRoutes, loadMenuData)
          asyncRoutes.push({ path: '*', redirect: '/', hidden: true })
          commit('SET_ROUTES', asyncRoutes)
          resolve(asyncRoutes)
        }
      }).catch(error => {
        console.log(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
