import http from '../../utils/http'
import { User } from '@/models'

const TOKEN_STORAGE_ITEM = 'polyphona-token'
const USER_STORAGE_ITEM = 'polyphona-user'

const getters = {
  getUser: state => state.user
}

const mutations = {
  setUser (state, user) {
    if (user) {
      localStorage.setItem(USER_STORAGE_ITEM, JSON.stringify(user))
    } else {
      localStorage.removeItem(USER_STORAGE_ITEM)
    }
    state.user = user
  },
  setToken (state, token) {
    localStorage.setItem(TOKEN_STORAGE_ITEM, token)
    http.defaults.headers.common['Authorization'] = 'Token ' + token
    state.token = token
  },
  discardToken () {
    localStorage.removeItem(TOKEN_STORAGE_ITEM)
  }
}

const actions = {
  async register (context, { username, firstName, lastName, password }) {
    const payload = {
      username,
      first_name: firstName,
      last_name: lastName,
      password
    }
    await http.post('/users/', payload)
    await context.dispatch('login', { username, password })
  },
  async login (context, { username, password }) {
    const resp = await http.post('/tokens/', { username, password })
    const { token, user: data } = resp.data
    const user = new User({
      username: data.username,
      firstName: data.first_name,
      lastName: data.last_name
    })
    context.commit('setToken', token)
    context.commit('setUser', user)
  },
  logout (context) {
    context.commit('discardToken')
    context.commit('setUser', null)
  }
}

// Initial state
const rawUser = localStorage.getItem(USER_STORAGE_ITEM)
const token = localStorage.getItem(TOKEN_STORAGE_ITEM)
if (token) {
  http.defaults.headers.common['Authorization'] = 'Token ' + token
}
const state = {
  user: rawUser ? new User(JSON.parse(rawUser)) : null,
  token
}

export default { namespaced: true, getters, actions, mutations, state }
