<template>
  <div id="home">
    <h1>Polyphona</h1>
    <p>
      <router-link to="login">Login</router-link>
    </p>
    <p>
      <router-link to="register">Create an account</router-link>
    </p>
    <p @click="save">
      Save
    </p>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import SongEditor from './SongEditor/SongEditor.vue'
  import store from '../store'
  export default {
    name: 'Home',
    components: { SongEditor },
    methods: {
      save () {
        this.$store.dispatch('MusicStore/getSavedTracks')
      }
    }
  }
  require('electron').ipcRenderer.on('saving', () => { store.dispatch('MusicStore/saveTrack') })
</script>

<style lang="scss" scoped>
  #home {
    height: 100%;
  }
</style>
