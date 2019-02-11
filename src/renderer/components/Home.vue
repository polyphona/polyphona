<template>
  <div id="home">
    <h1>Polyphona</h1>
    <div class="alert alert-primary alert-dismissable fade show" role="alert" v-if="isSaved">Le morceau est bien sauvé !
      <button type="button" class="close" @click="hideSuccessAlert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button> </div>
    <div class="alert alert-danger alert-dismissable fade show" role="alert" v-if="hasError">Le morceau n'a pas pu être sauvé !
      <button type="button" class="close" @click="hideErrorAlert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button> </div>
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
  export default {
    name: 'Home',
    components: { SongEditor },
    mounted: function () {
      require('electron').ipcRenderer.on('saving', () => {
        this.save()
      })
    },
    data () {
      return {isSaved: this.$store.state.MusicStore.saved,
        hasError: false }
    },

    methods: {
      async save () {
        await this.$store.dispatch('MusicStore/saveTrack').catch(() => {
          this.hasError = true
        })
        this.isSaved = this.$store.state.MusicStore.saved
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
