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
    <p @click="open">
      Open
    </p>
    <load-dialog v-if="showLoadDialog" v-on:close="showLoadDialog = false"></load-dialog>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import SongEditor from './SongEditor/SongEditor.vue'
  import store from '../store'
  import LoadDialog from './LoadDialog'

  export default {
    name: 'Home',
    components: {SongEditor, LoadDialog},
    methods: {
      save () {
        this.$store.dispatch('MusicStore/getSavedTracks')
      },
      open () {
        this.$store.dispatch('MusicStore/getSavedTracks')
        this.showLoadDialog = true
      }
    },
    data () {
      return {
        showLoadDialog: false
      }
    }
  }
  require('electron').ipcRenderer.on('saving', () => {
    store.dispatch('MusicStore/saveTrack')
  })
</script>

<style lang="scss" scoped>
  #home {
    height: 100%;
  }
</style>
