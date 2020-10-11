import apiConstant from './apiConstant'

export default {
  gzdaily (keywords, resolve, reject) {
    apiConstant.myAxios.post('reptile/gzdaily/', { 'keywords': keywords }).then(resolve, reject)
  },

  huxiu (keywords, resolve, reject) {
    apiConstant.myAxios.post('reptile/huxiu/', { 'keywords': keywords }).then(resolve, reject)
  },

  getResults (taskList, resolve, reject) {
    apiConstant.myAxios.get('reptile/results/', { params: taskList }).then(resolve, reject)
  }
}
