import axios from 'axios'

const http = axios.create({
  // NOTE (Florimond): I haven't found a way to read environment variables in Electron/Vue.
  baseURL: 'http://localhost:8000'
})

export default http
