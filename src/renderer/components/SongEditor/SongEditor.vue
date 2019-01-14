<template>
  <note-canvas id="note-canvas">
  </note-canvas>
</template>
<script>
  import NoteCanvas from './NoteCanvas.vue'

  export default {
    name: 'song-editor',
    components: {NoteCanvas}
  }
</script>
<style lang="scss" scoped>
  #note-canvas {
    width: 100%;
    height: 100%;
  }
</style>
