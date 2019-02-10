<template>
  <div id="home">
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
      load () {
        this.$store.dispatch('MusicStore/getSavedTracks')
        this.showLoadDialog = true
      }
    },
    data () {
      return {
        showLoadDialog: false
      }
    },
    mounted () {
      this.$electron.ipcRenderer.on('saving', () => {
        store.dispatch('MusicStore/saveTrack')
      })
      this.$electron.ipcRenderer.on('load', () => {
        this.load()
      })
    }
  }
</script>

<style lang="scss" scoped>
  #home {
    height: 100%;
  }
</style>
