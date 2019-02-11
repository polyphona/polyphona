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
      this.$electron.ipcRenderer.on('saving', () => {
        this.save()
      })
      this.$electron.ipcRenderer.on('load', () => {
        this.load()
      })
      // FIX: Electron may send the event multiple times, causing
      // the file selection window to show up multiple times.
      // So use `.once()` instead of `.on()` and rebind a once listener
      // in `.exportMidi()`.
      // See: (A)
      this.$electron.ipcRenderer.once('exportMidi', this.exportMidi)
    },
    data () {
      return {
        isSaved: this.$store.state.MusicStore.saved,
        hasError: false,
        showLoadDialog: false
      }
    },
    methods: {
      async save () {
        await this.$store.dispatch('MusicStore/saveTrack')
          .then(() => this.$store.dispatch('alerts/add', {
            kind: 'success',
            message: 'Le morceau est bien sauvé !'
          }))
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
        // (A)
        this.$store.dispatch('MusicStore/exportMidi')
        // Wait a bit so that the extra Electron events that will be sent
        // in a few ms are not caught.
        setTimeout(
          () => this.$electron.ipcRenderer.once('exportMidi', this.exportMidi),
          100
        )
      }
    }
  }
</script>

<style lang="scss" scoped>
  #home {
    height: 100%;
  }
</style>
