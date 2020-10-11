/* eslint-disable */
import axios from 'axios'
// import jsonpAdapter from 'axios-jsonp'
// const API_URL = 'https://private-674e2-reptile.apiary-mock.com'
const API_URL = 'http://129.204.168.148:8000/'
// const API_URL = 'http://139.199.71.21:8080/ordering/api/v1'

const myAxios = axios.create({
  baseURL: API_URL,
  timeout: 20000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  },
  withCredentials: false
})

export default {
  myAxios
}
