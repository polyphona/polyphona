<template>
  <div id="song-editor">
    <song-tool-bar></song-tool-bar>
    <note-canvas id="note-canvas"></note-canvas>
  </div>
</template>
<script>
  import NoteCanvas from './NoteCanvas.vue'
  import SongToolBar from './SongToolBar.vue'

  export default {
    name: 'song-editor',
    components: {NoteCanvas, SongToolBar}
  }
</script>
<style lang="scss" scoped>
    #song-editor {
        height: 100%;
    }
    #note-canvas {
        width: 100%;
        height: 100%;
    }
</style>
