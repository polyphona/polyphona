<template>
  <custom-track id="track"></custom-track>
</template>

<script>
  import CustomTrack from './MusicTrack/MusicTrack.vue'

  export default {
    name: 'landing-page',
    components: { CustomTrack }
  }
</script>

<style lang="scss" scoped>
  #track {
    height: 100vh;
  }
</style>

