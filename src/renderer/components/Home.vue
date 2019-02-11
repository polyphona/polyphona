<template>
  <div id="home">
    <div class="alert alert-primary alert-dismissable fade show" role="alert" v-if="isSaved">Le morceau est bien sauvé !
      <button type="button" class="close" @click="hideSuccessAlert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="alert alert-danger alert-dismissable fade show" role="alert" v-if="hasError">Le morceau n'a pas pu être
      sauvé !
      <button type="button" class="close" @click="hideErrorAlert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
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
    mounted () {
      this.$electron.ipcRenderer.on('saving', () => {
        this.save()
      })
      this.$electron.ipcRenderer.on('load', () => {
        this.load()
      })
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
        await this.$store.dispatch('MusicStore/saveTrack').catch(() => {
          this.hasError = true
        })
        this.isSaved = this.$store.state.MusicStore.saved
      },
      load () {
        this.$store.dispatch('MusicStore/getSavedTracks')
        this.showLoadDialog = true
      },
      hideSuccessAlert () {
        this.isSaved = false
      },
      hideErrorAlert () {
        this.hasError = false
      }
    }

  }
</script>

<style lang="scss" scoped>
  #home {
    height: 100%;
  }
</style>
