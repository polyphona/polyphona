<template>
  <div>
    <h1>Polyphona</h1>
    <p>
      <router-link to="login">Login</router-link>
    </p>
    <p>
      <router-link to="register">Create an account</router-link>
    </p>
    <song-editor></song-editor>
  </div>
</template>

<script>
  import SongEditor from './SongEditor/SongEditor.vue'

  export default {
    name: 'Home',
    components: { SongEditor }
  }
</script>

<style lang="scss" scoped>
</style>
