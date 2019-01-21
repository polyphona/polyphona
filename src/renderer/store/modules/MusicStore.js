import {Track, SCALE} from '../Music'

const division = 4
const scale = SCALE

const state = {
  currentTrack: new Track(),
  musicContext: {
    division,
    scale
  },
  renderContext: {
    // Percentage of the canvas filled by one tick, from 0 to 100.
    percentPerTick: 100 / (4 * division),
    // Percentage of the canvas filled by a note interval, from 0 to 100
    percentPerInterval: 100 / Object.keys(scale).length
  }
}

const mutations = {
  ADD_NOTE (state, note) {
    state.currentTrack.addNote(note)
  }
}

const getters = {
  listNotes: (state) => state.currentTrack.notes,
  getTrack: (state) => state.currentTrack,
  getRenderContext: (state) => state.renderContext,
  getMusicContext: (state) => state.musicContext
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
