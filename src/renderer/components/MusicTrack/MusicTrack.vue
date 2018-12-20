<template>
  <div class="wrapper">
    <note-canvas>
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
  import {NoteCanvasAdapter} from '@/store/Music.js'
  import {mapGetters} from 'vuex'
  import NoteCanvas from './NoteCanvas.vue'
  import NoteBox from './NoteBox.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'custom-track',
    components: {NoteCanvas, NoteBox},
    methods: {},
    computed: {
      noteBoxes () {
        return this.listNotes.map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      },
      ...mapGetters(['listNotes'])}
  }
</script>
<style lang="scss" scoped>
  .wrapper {
    display: grid;
    grid-template-rows: auto 1fr;
    grid-template-columns: 1fr;
  }
</style>
