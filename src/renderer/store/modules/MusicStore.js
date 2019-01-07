import {Track} from '../Music'

const state = {
  currentTrack: new Track()
}

const mutations = {
  ADD_NOTE (state, note) {
    state.currentTrack.addNote(note)
  }
}

const getters = {
  listNotes: state => state.currentTrack.notes
}

const actions = {
  addNote (context, note) {
    context.commit('ADD_NOTE', note)
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
}
