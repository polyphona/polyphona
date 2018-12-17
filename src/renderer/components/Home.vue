<template>
  <div>
    <h1>Polyphona</h1>
    <p>
      <router-link to="login">Login</router-link>
    </p>
    <custom-track></custom-track>
  </div>
</template>

<script>
  import CustomTrack from './MusicTrack/MusicTrack.vue'

  export default {
    name: 'Home',
    components: { CustomTrack }
  }
</script>

<style lang="scss" scoped>

</style>
