<template>
  <div id="home">
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
  #home {
    height: 100%;
  }
</style>
