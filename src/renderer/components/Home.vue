<template>
  <div id="home">
    <alerts-list></alerts-list>
    <load-dialog v-if="showLoadDialog" v-on:close="showLoadDialog = false"></load-dialog>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import SongEditor from './SongEditor/SongEditor.vue'
  import LoadDialog from './LoadDialog'
  import AlertsList from './AlertsList.vue'

  export default {
    name: 'Home',
    components: {SongEditor, LoadDialog, AlertsList},
    mounted () {
      this.$electron.ipcRenderer.on('saving', this.save)
      this.$electron.ipcRenderer.on('load', this.load)
      this.$electron.ipcRenderer.on('exportMidi', this.exportMidi)
      this.$electron.ipcRenderer.on('importMidi', this.importMidi)
    },
    data () {
      return {
        hasError: false,
        showLoadDialog: false
      }
    },
    methods: {
      save () {
        this.$store.dispatch('MusicStore/saveTrack')
          .then(() => {
            this.$store.dispatch('alerts/add', {
              kind: 'success',
              message: 'Le morceau est bien sauvé !'
            })
          })
          .catch(() => {
            this.$store.dispatch('alerts/add', {
              kind: 'danger',
              message: "Le morceau n'a pas pu être sauvé !"
            })
          })
      },
      load () {
        this.$store.dispatch('MusicStore/getSavedTracks')
        this.showLoadDialog = true
      },
      exportMidi () {
        this.$store.dispatch('MusicStore/exportMidi')
      },
      importMidi () {
        this.$store.dispatch('MusicStore/importMidi')
      }
    },
    destroyed () {
      this.$electron.ipcRenderer.removeAllListeners('saving')
      this.$electron.ipcRenderer.removeAllListeners('load')
      this.$electron.ipcRenderer.removeAllListeners('importMidi')
      this.$electron.ipcRenderer.removeAllListeners('exportMidi')
    }
  }
</script>

<style lang="scss" scoped>
  #home {
    height: 70%;
  }
</style>
