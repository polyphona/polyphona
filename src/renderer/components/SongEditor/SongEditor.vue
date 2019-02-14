<template>
  <div id="song-editor">
    <form id="song-tools">
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
    <note-canvas id="note-canvas"></note-canvas>
  </div>
</template>
<script>
  import NoteCanvas from './NoteCanvas.vue'

  export default {
    name: 'song-editor',
    components: {NoteCanvas},
    destroyed () {
      // Prevent music from keeping playing when navigating to another page.
      this.$store.dispatch('music/stop')
    },
    methods: {
      togglePlay () {
        this.$store.dispatch('music/togglePlay')
      },
      exportMidi () {
        this.$store.dispatch('music/exportMidi')
      },
      importMidi () {
        this.$store.dispatch('music/importMidi')
      }
    },
    computed: {
      title: {
        get () {
          return this.$store.getters['music/getTrack'].name
        },
        set (value) {
          this.$store.dispatch('music/setTrackName', value)
        }
      },
      octave: {
        get () {
          return this.$store.getters['music/getOctave']
        },
        set (value) {
          this.$store.dispatch('music/updateOctave', value)
        }
      },
      playing () {
        return this.$store.getters['music/getPlaying']
      }
    }
  }
</script>
<style lang="scss" scoped>
    #song-editor {
        height: 100%;
    }

    #song-tools {
        padding: 1em;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    #note-canvas {
        width: 100%;
        height: 100%;
    }
</style>
