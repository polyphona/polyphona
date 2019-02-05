<template>
  <div id="song-editor">
    <p style="display: flex;">
      <span class="form-field">
        <button @click="togglePlay">{{ playing ? '❙❙' : '►️'}}️</button>
      </span>
      <span class="form-field">
        <label for="octave">Octave:</label>
        <select id="octave" v-model="octave">
          <option :value="1">1</option>
          <option :value="2">2</option>
          <option :value="3">3</option>
          <option :value="4">4</option>
          <option :value="5">5</option>
          <option :value="6">6</option>
        </select>
      </span>
    </p>
    <note-canvas id="note-canvas"></note-canvas>
  </div>
</template>
<script>
  import NoteCanvas from './NoteCanvas.vue'

  export default {
    name: 'song-editor',
    components: {NoteCanvas},
    methods: {
      togglePlay () {
        this.$store.dispatch('MusicStore/togglePlay')
      }
    },
    computed: {
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

  #note-canvas {
    width: 100%;
    height: 100%;
  }

  .form-field {
    margin: 1em;
  }
</style>
