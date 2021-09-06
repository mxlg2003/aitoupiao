import store from '@/store'

export default {
  inserted(el, binding, vnode) {
    const { value } = binding
    const permissions = store.getters && store.getters.permisaction

    if (value && value instanceof Array && value.length > 0) {
      const permissionFlag = value
      console.log('去除操作权限控制')
      // const hasPermissions = permissions.some(permission => {
      //   return permissionFlag.includes(permission)
      // })
      //
      // if (!hasPermissions) {
      //   el.parentNode && el.parentNode.removeChild(el)
      // }
    }
  }
}
