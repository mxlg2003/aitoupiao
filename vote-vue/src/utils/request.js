import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
const Base64 = require('js-base64').Base64

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 10000
})

// 请求拦截器 - 请求头预处理
service.interceptors.request.use(
  config => {
    config.headers['TokenCheck'] =  Base64.encode((Math.floor(Math.random() * (90 - 10)) + 10).toString()) + '-' + Base64.encode('JK') + '-' + Base64.encode((new Date()).valueOf())
    if (store.getters.token) {
      config.headers['token'] = store.getters.token
    }
    return config
  },
  error => {
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// 返回拦截器 - 返回参数预处理
service.interceptors.response.use(
  response => {
    const res = response.data;
    if (res.detail) {
      res.code = res.detail.code
      res.message = res.detail.message
      return res
    }
    if (res.code === 401) {
      Message({
        message: res.message,
        type: 'error',
        duration: 5 * 1000
      })
      return res
    }
    if (res.code !== 200) {
      if (res.code === 402) {
        setTimeout(() => {
          MessageBox.confirm('登录失效或者账号在其他设备登录, 请重新登录', '确定', {
            confirmButtonText: '重新登陆',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            store.dispatch('user/LogOut').then(() => {
              location.reload()
            })
          }).catch(() => {
            Message({
              type: 'info',
              message: '关闭'
            });
          });
        }, 500)
        return
      }
      if (res.code === 50008 || res.code === 50012 || res.code === 50014 || res.code === 403) {
        MessageBox.confirm('您已经退出登录，请重新登录', '确定', {
          confirmButtonText: '重新登陆',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/LogOut').then(() => {
            location.reload()
          })
        }).catch(() => {
          Message({
            type: 'info',
            message: '关闭'
          });
        });
      }
      if (res.code === 400) {
        Message({
          type: 'error',
          message: res.message
        });
        return
      }
      if (res.code === 404){
        Message({
          type: 'error',
          message: res.message
        });
        return
      }
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res
  },
  error => {
    Message({
      message: error.res.data.message,
      type: 'error',
      duration: 5 * 1000
    })

    setTimeout(() => {
      if (error.res.data.code === 403) {
        MessageBox.confirm('登录失效或已在其他设备登录，请重新登录', '确定', {
          confirmButtonText: '重新登陆',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/LogOut').then(() => {
            location.reload()
          })
        }).catch(() => {
          Message({
            type: 'info',
            message: '关闭'
          });
        });
      }
    }, 500)

    return Promise.reject(error);

  }
)

export default service
