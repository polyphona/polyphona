import {Track} from '../Music'

const state = {
  currentTrack: new Track()
}

const mutations = {
  setAddNote (state, note) {
    console.log('here')
    state.currentTrack.addNote(note)
  }
}

const getters = {
  listNotes: state => state.currentTrack.notes
}

const actions = {
  addNote (context, note) {
    console.log('hiya')
    context.commit('setAddNote', note)
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
}
