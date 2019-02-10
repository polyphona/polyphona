import Tone from 'tone'
import http from '../../utils/http'
import {Track, SCALE} from '../Music'

const division = 4
const scale = SCALE
// NOTE: synthesizer cannot be in the store because Tone modifies this value
// (and does so outside of a mutation, which Vuex does not like).
const synthesizer = new Tone.PluckSynth().toMaster()
Tone.Transport.bpm.value = 120

const state = {
  currentTrack: new Track(),
  musicContext: {
    division,
    scale,
    octave: 4,
    playing: false
  },
  // Mapping of note IDs to transport event IDs.
  // Used to un-schedule an event when a note is deleted.
  schedule: new Map(),
  renderContext: {
    // Percentage of the canvas filled by one tick, from 0 to 100.
    percentPerTick: 100 / (4 * division),
    // Percentage of the canvas filled by a note interval, from 0 to 100
    percentPerInterval: 100 / Object.keys(scale).length
  },
  savedTracks: [],
  saved: false
}

function toTransportTime (musicContext, canvasTime) {
  // Notation: "bar:quarter:sixteenth"
  // See: https://github.com/Tonejs/Tone.js/wiki/Time#transport-time
  const quarter = Math.floor(canvasTime / musicContext.division)
  const sixteenth = 4 / musicContext.division * (canvasTime % musicContext.division)
  return `0:${quarter}:${sixteenth}`
}

const mutations = {
  ADD_NOTE (state, note) {
    state.currentTrack.addNote(note)
    state.saved = false
  },
  DELETE_NOTE (state, note) {
    state.currentTrack.deleteNote(note)
    const eventId = state.schedule.get(note.id)
    if (eventId) {
      Tone.Transport.clear(eventId)
    }
    state.saved = false
  },
  SCHEDULE_NOTES (state) {
    state.currentTrack.notes.forEach((note) => {
      const pitch = state.musicContext.scale[note.pitch] + state.musicContext.octave
      const trigger = (time) => synthesizer.triggerAttackRelease(pitch, toTransportTime(note.duration), time)
      const eventId = Tone.Transport.schedule(trigger, toTransportTime(state.musicContext, note.startTime))
      state.schedule.set(note.id, eventId)
    })
  },
  TOGGLE_PLAY (state) {
    state.musicContext.playing = !state.musicContext.playing
  },
  SET_OCTAVE (state, octave) {
    state.musicContext.octave = octave
  },
  SAVE (state, res) {
    state.currentTrack.remoteId = res.id
    state.saved = true
  },
  SAVED_TRACKS (state, savedTracks) {
    state.savedTracks = savedTracks
  },
  LOAD_TRACK (state, track, id) {
    state.currentTrack = track
    state.currentTrack.remoteId = id
  }
}

const getters = {
  listNotes: (state) => state.currentTrack.notes,
  getTrack: (state) => state.currentTrack,
  getRenderContext: (state) => state.renderContext,
  getMusicContext: (state) => state.musicContext,
  getOctave: (state) => state.musicContext.octave,
  getPlaying: (state) => state.musicContext.playing
}

const actions = {
  addNote (context, note) {
    context.commit('ADD_NOTE', note)
    context.dispatch('restart')
    context.state.saved = false
  },
  deleteNote (context, note) {
    context.commit('DELETE_NOTE', note)
    context.dispatch('restart')
    context.state.saved = false
  },
  play (context, offset) {
    context.commit('SCHEDULE_NOTES')
    // Loop one measure ad eternam
    Tone.Transport.loopEnd = '1m'
    Tone.Transport.loop = true
    // Start the song now, but offset by `offset`.
    Tone.Transport.start(Tone.Transport.now(), offset)
  },
  restart (context) {
    if (context.state.musicContext.playing) {
      const offset = Tone.Transport.getSecondsAtTime()
      Tone.Transport.stop()
      context.dispatch('play', offset)
    }
  },
  togglePlay (context) {
    if (context.state.musicContext.playing) {
      Tone.Transport.stop()
    } else {
      context.dispatch('play')
    }
    context.commit('TOGGLE_PLAY')
  },
  updateOctave (context, octave) {
    context.commit('SET_OCTAVE', octave)
    context.dispatch('restart')
  },
  async saveTrack ({state, commit}) {
    const data = {
      'name': state.currentTrack.name,
      'tracks': [state.currentTrack]
    }
    const {data: res} = state.currentTrack.remoteId ? await http.put('songs/' + state.currentTrack.remoteId, data) : await http.post('songs', data)
    commit('SAVE', res)
  },
  async getSavedTracks ({state, commit, rootState}) {
    const {data: res} = await http.get('users/' + rootState.auth.user.username + '/songs')
    console.log(res)
    commit('SAVED_TRACKS', res)
  },
  loadSavedTrack ({state, commit}, id) {
    const track = state.savedTracks.find(track => track.id === id)
    commit('LOAD_TRACK', track, id)
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
}
