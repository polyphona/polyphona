<template>
  <div id="home">
    <load-dialog v-if="showLoadDialog" v-on:close="showLoadDialog = false"></load-dialog>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import SongEditor from './SongEditor/SongEditor.vue'
  import LoadDialog from './LoadDialog'

  export default {
    name: 'Home',
    components: {SongEditor, LoadDialog},
    data () {
      return {
        showLoadDialog: false
      }
    },
    mounted () {
      this.$electron.ipcRenderer.on('saving', () => {
        this.$store.dispatch('MusicStore/saveTrack')
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
    methods: {
      save () {
        this.$store.dispatch('MusicStore/getSavedTracks')
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
