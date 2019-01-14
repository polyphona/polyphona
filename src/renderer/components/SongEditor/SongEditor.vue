<template>
    <note-canvas id="note-canvas"
                 @canvas-click="onCanvasClick"
                 @canvas-mousedown="onCanvasMouseDown"
                 @canvas-mousedrag="onCanvasMouseDrag"
                 @canvas-mouseup="onCanvasMouseUp"
                 @canvas-mouseleave="onCanvasMouseLeave"
    >
        <note-box
                v-if="newBox"
                :x="newBox.x"
                :y="newBox.y"
                :width="newBox.width"
                :height="newBox.height"
                :color="'#afa'"
                layer="foreground"
        ></note-box>
        <note-box
                v-for="box in noteBoxes"
                :key="box.id"
                :x="box.x"
                :y="box.y"
                :width="box.width"
                :height="box.height"
                :color="'#0f0'"
        ></note-box>
    </note-canvas>
</template>
<script>
  import {Track, NoteCanvasAdapter, NoteTooSmallException} from './Music.js'
  import NoteCanvas from './NoteCanvas.vue'
  import NoteBox from './NoteBox.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'song-editor',
    components: {NoteCanvas, NoteBox},
    data () {
      const track = new Track(4, 1)
      return {
        track,
        newBox: null,
        renderContext: {
          // Percentage of the canvas filled by a quarter note,
          // i.e. 1/4th of a bar.
          percentPerQuarter: 10,
          // Percentage of the canvas filled by a note interval,
          // i.e. the difference in pitch between A and A#
          percentPerInterval: 20
        }
      }
    },
    methods: {
      addNoteFromBox (box) {
        try {
          const note = canvasAdapter.toNote(this.renderContext, box)
          this.track.addNote(note)
          return note
        } catch (e) {
          if (e instanceof NoteTooSmallException) {
            return
          }
          throw e
        }
      },
      onCanvasClick ({x, y}) {
        let box = {
          x,
          y,
          width: this.renderContext.percentPerQuarter,
          height: this.renderContext.percentPerInterval
        }
        console.log(this.track.notes)
        box = canvasAdapter.clip(this.renderContext, box)
        const note = canvasAdapter.toNote(this.renderContext, box)
        const existingNote = this.track.notes.find((value) => note.equals(value))
        if (existingNote) {
          this.track.deleteNote(existingNote)
        } else {
          this.addNoteFromBox(box)
        }
      },
      onCanvasMouseDown ({x, y}) {
        const height = this.renderContext.percentPerInterval
        const width = 0
        const box = {x, y, width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onCanvasMouseDrag ({x}) {
        this.newBox.width = x - this.newBox.x
        this.newBox = canvasAdapter.clip(this.renderContext, this.newBox)
      },
      onCanvasMouseUp () {
        this.addNoteFromBox(this.newBox)
        this.newBox = null
      },
      onCanvasMouseLeave () {
        this.newBox = null
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
    #note-canvas {
        width: 100%;
        height: 100%;
    }
</style>
