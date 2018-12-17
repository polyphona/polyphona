<template>
  <div class="wrapper">
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
  import {Track, NoteCanvasAdapter} from './Music.js'
  import NoteCanvas from './NoteCanvas.vue'
  import NoteBox from './NoteBox.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'custom-track',
    components: {NoteCanvas, NoteBox},
    data () {
      const track = new Track(4, 1)
      return {
        track,
        renderContext: {
          // Percentage of the canvas filled by a quarter note,
          // i.e. 1/4th of a bar
          percentPerQuarter: 10,
          // Percentage of the canvas filled by a note interval,
          // i.e. the difference in pitch between A and A#
          percentPerInterval: 25
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
