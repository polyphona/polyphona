import Vue from 'vue'
import Vuex from 'vuex'

import { createPersistedState, createSharedMutations } from 'vuex-electron'

// import modules from './modules'
import MusicStore from './modules/MusicStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    MusicStore: MusicStore
  },
  plugins: [
    createPersistedState(),
    createSharedMutations()
  ],
  strict: process.env.NODE_ENV !== 'production'
})
