import { login, logout, getUserInfo } from '@/api/login'
import { setToken, getToken, removeToken } from '@/utils/cookie-token'
import storage from '@/utils/storage'

const state = {
  token: getToken(),
  name: '',
  roles: [],
  permissions: [],
  permisaction: []
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_PERMISSIONS: (state, permisaction) => {
    state.permisaction = permisaction
  }
}

const actions = {
  // 执行登录
  login({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      login(userInfo).then(response => {
        if (response.code === 200) {
          const token = response.token
          commit('SET_TOKEN', token)
          setToken(token)
          resolve()
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 获取当前用户信息
  getUserInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getUserInfo().then(response => {
        if (response.code !== 200) {
          commit('SET_TOKEN', '')
          removeToken(getToken())
          reject('error')
        }
        const { user_name, permissions } = response.user
        commit('SET_PERMISSIONS', permissions)
        commit('SET_ROLES', ['admin'])
        commit('SET_NAME', user_name)
        resolve(response.user)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 退出系统
  LogOut({ commit }) {
    return new Promise((resolve, reject) => {
      logout({}).then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        commit('SET_PERMISSIONS', [])
        removeToken(getToken())
        storage.clear()
        resolve()
      }).catch(error => {
        reject(error)
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
