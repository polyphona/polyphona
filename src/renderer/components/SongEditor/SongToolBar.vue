<template>
  <form>
    <span class="form-field">
      <button class="btn btn-light" @click="togglePlay" type="button">{{ playing ? '❙❙' : '►️'}}️</button>
      <button class="btn btn-light" @click="exportMidi" type="button">📂 Export</button>
      <button class="btn btn-light" @click="importMidi" type="button">📥 Import</button>
    </span>
    <span class="form-group">
      <label for="title">Title:</label>
      <input
        id="title"
        class="form-control"
        type="text"
        required
        placeholder="Enter a song title…"
        v-model="title"
      >
    </span>
    <span class="form-group">
      <label for="octave">Octave:</label>
      <input
        id="octave"
        class="form-control"
        type="number"
        min="1"
        max="6"
        required
        v-model="octave"
      >
    </span>
  </form>
</template>

<script>
import {mapActions} from 'vuex'

export default {
  name: 'song-tool-bar',
  computed: {
    title: {
      get () {
        return this.$store.getters['MusicStore/getTrack'].name
      },
      set (value) {
        this.$store.dispatch('MusicStore/setTrackName', value)
      }
    },
    octave: {
      get () {
        return this.$store.getters['MusicStore/getOctave']
      },
      set (value) {
        this.$store.dispatch('MusicStore/updateOctave', value)
      }
    },
    playing () {
      return this.$store.getters['MusicStore/getPlaying']
    }
  },
  methods: {
    ...mapActions('MusicStore', ['togglePlay', 'exportMidi', 'importMidi'])
  },
  destroyed () {
    // Prevent music from keeping playing when navigating to another page.
    this.$store.dispatch('MusicStore/stop')
  }
}
</script>

<style lang="scss" scoped>
form {
  padding: 0 1em;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>

