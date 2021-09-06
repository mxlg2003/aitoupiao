import Vue from 'vue'
import axios from 'axios'

const vm = new Vue()
const isNewVersion = () => {
  const url = `//${window.location.host}/version.json?t=${new Date().getTime()}`
  axios.get(url).then(res => {
    if (res.status === 200) {
      const vueVersion = res.data.version
      const localVueVersion = localStorage.getItem('vueVersion')
      if (localVueVersion && localVueVersion !== vueVersion) {
        localStorage.setItem('vueVersion', vueVersion)
        window.location.reload()
        return
      } else {
        localStorage.setItem('vueVersion', vueVersion)
      }
    }
  })
}

export default {
  isNewVersion
}
