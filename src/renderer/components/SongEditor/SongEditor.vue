<template>
  <div id="song-editor">
    <form id="song-tools">
      <span class="form-field">
        <button class="btn btn-light" @click="togglePlay" type="button">{{ playing ? '❙❙' : '►️'}}️</button>
        <button class="btn btn-light" @click="exportMidi" type="button">📂 Export</button>
        <button class="btn btn-light" @click="importMidi" type="button">📂 Import</button>
      </span>
      <span class="form-group">
        <label for="title">Title:</label>
        <input id="title" class="form-control" type="text" required v-model="title">
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
      this.$store.dispatch('MusicStore/stop')
    },
    methods: {
      togglePlay () {
        this.$store.dispatch('MusicStore/togglePlay')
      },
      exportMidi () {
        this.$store.dispatch('MusicStore/exportMidi')
      },
      importMidi () {
        this.$store.dispatch('MusicStore/importMidi')
      }
    },
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
    }
  }
</script>
<style lang="scss" scoped>
    #song-editor {
        height: 70%;
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
