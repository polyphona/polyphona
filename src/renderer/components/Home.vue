<template>
  <div id="home">
    <alerts-list></alerts-list>
    <load-dialog v-if="showLoadDialog" @close="showLoadDialog = false"></load-dialog>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import {mapActions} from 'vuex'
  import SongEditor from './SongEditor/SongEditor.vue'
  import LoadDialog from './LoadDialog'
  import AlertsList from './AlertsList.vue'

  export default {
    name: 'Home',
    components: {SongEditor, LoadDialog, AlertsList},
    mounted () {
      // See: https://electronjs.org/docs/api/ipc-renderer
      this.$electron.ipcRenderer.on('saving', this.save)
      this.$electron.ipcRenderer.on('load', this.load)
      this.$electron.ipcRenderer.on('exportMidi', this.exportMidi)
      this.$electron.ipcRenderer.on('importMidi', this.importMidi)
    },
    data () {
      return {
        showLoadDialog: false
      }
    },
    methods: {
      save () {
        this.$store.dispatch('music/saveTrack')
          .then(() => {
            this.$store.dispatch('alerts/add', {
              kind: 'success',
              message: 'Le morceau est bien sauvé !'
            })
          })
          .catch(() => {
            this.$store.dispatch('alerts/add', {
              kind: 'danger',
              message: "Le morceau n'a pas pu être sauvé…"
            })
          })
      },
      load () {
        this.$store.dispatch('music/getSavedTracks')
        this.showLoadDialog = true
      },
      ...mapActions('music', ['exportMidi', 'importMidi'])
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
