import {Track} from '../Music'

const state = {
  currentTrack: new Track()
}

const mutations = {
  ADD_NOTE (state, note) {
    console.log('here')
    state.currentTrack.addNote(note)
  }
}

const getters = {
  listNotes: state => state.currentTrack.notes
}

const actions = {
  addNote: ({commit}, note) => { console.log('hiya'); commit('ADD_NOTE', note) }
}

export default {
  state,
  mutations,
  getters,
  actions
}
