import {Track} from '../Music'
import http from '../../utils/http'

const state = {
  currentTrack: new Track(),
  saved: false
}

const mutations = {
  ADD_NOTE (state, note) {
    state.currentTrack.addNote(note)
  },
  DELETE_NOTE (state, note) {
    state.currentTrack.deleteNote(note)
  }
}

const getters = {
  listNotes: state => state.currentTrack.notes
}

const actions = {
  addNote ({commit}, note) {
    commit('ADD_NOTE', note)
  },
  deleteNote ({commit}, note) {
    commit('DELETE_NOTE', note)
  },
  async saveTrack ({state}, note) {
    const data = {
      'name': 'Test',
      'tracks': state.currentTrack
    }
    await http.post('songs', data)
    state.currentTrack.saved = true
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
}
