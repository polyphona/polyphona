import fs from 'fs'
import {remote} from 'electron'
import * as MidiConvert from 'simonadcock-midiconvert'
import Tone from 'tone'
import {Track, SCALE, TrackLoader} from '../Music'
import http from '../../utils/http'

// NOTE: synthesizer cannot be in the store because Tone modifies this value
// (and does so outside of a mutation, which Vuex does not like).
const synthesizer = new Tone.PolySynth().toMaster()
Tone.Transport.bpm.value = 120

class RenderContext {
  constructor (musicContext) {
    this.musicContext = musicContext
  }

  get percentPerTick () {
    return 100 / this.musicContext.bars / (4 * this.musicContext.division)
  }

  get percentPerInterval () {
    return 100 / Object.keys(this.musicContext.scale).length
  }
}

class MusicContext {
  constructor () {
    this.division = 4
    this.scale = SCALE
    this.octave = 2
    this.bars = 2
    this.playing = false
  }

  toTransportTime (canvasTime) {
    // Notation: "bar:quarter:sixteenth"
    // See: https://github.com/Tonejs/Tone.js/wiki/Time#transport-time
    let quarter = Math.floor(canvasTime / this.division)
    const bars = Math.floor(quarter / 4)
    quarter -= 4 * bars
    const sixteenth = 4 / this.division * (canvasTime % this.division)
    return `${bars}:${quarter}:${sixteenth}`
  }
}

class State {
  constructor () {
    this.currentTrack = new Track()
    this.musicContext = new MusicContext()
    this.renderContext = new RenderContext(this.musicContext)
    this.savedTracks = []
    this.saved = false
  }
}

const state = new State()

const getters = {
  listNotes: (state) => state.currentTrack.notes,
  getTrack: (state) => state.currentTrack,
  getRenderContext: (state) => state.renderContext,
  getMusicContext: (state) => state.musicContext,
  getOctave: (state) => state.musicContext.octave,
  getPlaying: (state) => state.musicContext.playing
}

const mutations = {
  ADD_NOTE (state, note) {
    state.currentTrack.addNote(note)
    state.saved = false
  },
  DELETE_NOTE (state, note) {
    state.currentTrack.deleteNote(note)
    state.saved = false
  },
  SCHEDULE_NOTES (state) {
    state.currentTrack.notes.forEach((note) => {
      const pitch = (
        state.musicContext.scale[note.pitch] + state.musicContext.octave
      )
      Tone.Transport.schedule(
        (time) => {
          synthesizer.triggerAttackRelease(
            pitch,
            state.musicContext.toTransportTime(note.duration),
            time,
            note.velocity
          )
        },
        state.musicContext.toTransportTime(note.startTime)
      )
    })
  },
  START (state) {
    state.musicContext.playing = true
  },
  STOP (state) {
    state.musicContext.playing = false
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
  LOAD_TRACK (state, {track, id}) {
    state.currentTrack = TrackLoader.toTrack(track)
    state.currentTrack.remoteId = id
  }
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
  play ({commit, state}, offset) {
    commit('START')
    commit('SCHEDULE_NOTES')
    Tone.Transport.loopEnd = `${state.musicContext.bars}m`
    Tone.Transport.loop = true
    // Start the song now, but offset by `offset`.
    Tone.Transport.start(Tone.Transport.now(), offset)
  },
  stop ({commit}) {
    commit('STOP')
    Tone.Transport.stop()
    // Cancel all note events so they are not played again
    // when the transport starts again.
    Tone.Transport.cancel()
  },
  restart (context) {
    if (context.state.musicContext.playing) {
      const offset = Tone.Transport.getSecondsAtTime()
      context.dispatch('stop')
      context.dispatch('play', offset)
    }
  },
  togglePlay (context) {
    if (context.state.musicContext.playing) {
      context.dispatch('stop')
    } else {
      context.dispatch('play')
    }
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
    commit('SAVED_TRACKS', res)
  },
  loadSavedTrack ({state, commit}, id) {
    const track = state.savedTracks.find(track => track.id === id)
    commit('LOAD_TRACK', {track: track.tracks[0], id}) // Not good but necessary, will change when we upgrade the local song model
  },
  exportMidi ({dispatch, state}) {
    const midi = MidiConvert.create()

    // TODO: make channel/instrument customizable
    const channel = 32
    const track = midi.track().patch(channel)

    const toMidiTime = (canvasTime) => (
      canvasTime /
      state.musicContext.division /
      (Tone.Transport.bpm.value / 60)
    )

    state.currentTrack.notes.forEach((note) => {
      const pitch = (
        state.musicContext.scale[note.pitch].toLowerCase() + state.musicContext.octave.toString()
      )
      track.note(
        pitch,
        toMidiTime(note.startTime),
        toMidiTime(note.duration),
        note.velocity
      )
    })

    const path = remote.dialog.showSaveDialog({
      'filters': [
        {
          'name': 'MIDI',
          'extensions': ['midi']
        }
      ]
    })
    if (!path) {
      return
    }

    fs.writeFileSync(path, midi.encode(), 'binary')

    dispatch('alerts/add', {
      kind: 'success',
      message: `Le morceau a été exporté sous ${path}.`
    }, {root: true})
  }
}

export default {
  namespaced: true,
  state: state,
  mutations: mutations,
  getters: getters,
  actions: actions
}
