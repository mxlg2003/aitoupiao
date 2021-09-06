import storage from '@/utils/storage'

export default function getPageTitle(pageTitle) {
  const app_info = storage.get('app_info')
  const title = app_info ? app_info.name : '爱投票管理系统'
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
