<template>
  <div class="wrapper">
    <h1>My music track</h1>
    <note-canvas @canvas-click="onClickCanvas">
      <note-box
        v-for="box in noteBoxes"
        :x="box.x"
        :y="box.y"
        :width="box.width"
        :height="box.height"
        :color="'#0f0'"
      ></note-box>
    </note-canvas>
  </div>
</template>
<script>
  import {Track, Note, NoteCanvasAdapter} from './Music.js'
  import NoteCanvas from './NoteCanvas.vue'
  import NoteBox from './NoteBox.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'custom-track',
    components: {NoteCanvas, NoteBox},
    data () {
      const track = new Track(4, 1)
      track.addNote(new Note(0.5, 4, 3))
      track.addNote(new Note(2, 1, 0))
      return {
        track,
        renderContext: {
          percentPerQuarter: 10,
          percentPerInterval: 10
        }
      }
    },
    methods: {
      onClickCanvas ({x, y}) {
        const box = {x, y, width: 10, height: 10}
        const note = canvasAdapter.toNote(this.renderContext, box)
        this.track.addNote(note)
      }
    },
    computed: {
      noteBoxes () {
        return this.track.notes.map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      }
    }
  }
</script>
<style lang="scss" scoped>
  .wrapper {
    display: grid;
    grid-template-rows: auto 1fr;
    grid-template-columns: 1fr;
  }
</style>
