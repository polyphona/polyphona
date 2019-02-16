<template>
  <div class="wrapper">
    <pitch-header></pitch-header>

    <canvas-layers
      class="canvas-wrapper"
      :names="layerNames"
      @resized="canvasId++"
      @click="onClick"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mousemove="onMouseMove"
      @mouseleave="onMouseLeave"
    >
      <progress-bar layer="decorations"></progress-bar>

      <note-grid layer="background" :key="canvasId"></note-grid>

      <!-- Note being created (if any) -->
      <note-box
        v-if="newBox"
        :x="newBox.x"
        :y="newBox.y"
        :width="newBox.width"
        :height="newBox.height"
        :color="'#ffe17f'"
        layer="foreground"
      ></note-box>

      <!-- Notes in the song. -->
      <note-box
        v-for="box in noteBoxes"
        :key="canvasId + '-note-' + box.id"
        :x="box.x"
        :y="box.y"
        :width="box.width"
        :height="box.height"
        :color="'#f6cd4c'"
        layer="notes"
      ></note-box>
    </canvas-layers>
  </div>
</template>

<script>
  import {NoteCanvasAdapter} from './adapters'
  import {NoteTooSmallException} from './errors'
  import CanvasLayers from './CanvasLayers.vue'
  import NoteBox from './NoteBox'
  import CanvasLine from './CanvasLine.vue'
  import ProgressBar from './ProgressBar.vue'
  import NoteGrid from './NoteGrid.vue'
  import PitchHeader from './PitchHeader.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  const DRAG_RIGHT = 1
  const DRAG_NONE = 0
  const DRAG_LEFT = -1

  export default {
    name: 'NoteCanvas',
    components: {CanvasLayers, NoteBox, CanvasLine, ProgressBar, NoteGrid, PitchHeader},
    data () {
      return {
        newBox: null,
        // Determines whether we're dragging a new note,
        // and in which direction.
        dragging: false,
        clicking: false,
        layerNames: ['background', 'notes', 'decorations', 'foreground'],
        // Gets incremented when the canvas has been resized and
        // needs to be re-rendered.
        canvasId: 0
      }
    },
    computed: {
      noteBoxes () {
        return this.$store.getters['music/listNotes'].map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      },
      renderContext () {
        return this.$store.getters['music/getRenderContext']
      }
    },
    methods: {
      addNoteFromBox (box) {
        try {
          const note = canvasAdapter.toNote(this.renderContext, box)
          this.$store.dispatch('music/addNote', note)
          return note
        } catch (e) {
          if (e instanceof NoteTooSmallException) {
            return
          }
          throw e
        }
      },
      onClick ({x, y}) {
        if (!this.clicking) {
          return
        }
        let box = {
          x,
          y,
          width: this.renderContext.percentPerTick,
          height: this.renderContext.percentPerInterval
        }
        box = canvasAdapter.clip(this.renderContext, box)
        const note = canvasAdapter.toNote(this.renderContext, box)
        const existingNote = this.$store.getters['music/listNotes'].filter((value) => note.disturbs(value))
        if (existingNote.length > 0) { // There is an existing note : we delete note
          this.$store.dispatch('music/deleteNote', existingNote[0])
        } else { // there are no problematic notes : we add a new note
          this.addNoteFromBox(box)
        }
        this.clicking = false
      },
      onMouseDown ({x, y}) {
        this.clicking = true
        this.dragging = DRAG_NONE
        const height = this.renderContext.percentPerInterval
        const width = this.renderContext.percentPerTick
        const box = {x, y, width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onMouseMove ({x, y}) {
        this.clicking = false
        if (this.dragging === false) {
          return
        }

        const eventX = x
        // Perform a bit of logic to keep track of which way we are
        // dragging the note.
        // This is necessary in order to correctly draw the new note,
        // especially for it to have a correct X coordinate.
        if (eventX - this.newBox.x > 0) {
          // Now dragging to the right.
          if (this.dragging === DRAG_LEFT) {
            // Fix the X coordinate.
            this.newBox.x -= this.renderContext.percentPerTick
          }
          this.dragging = DRAG_RIGHT
        } else {
          // Now dragging to the left.
          if (this.dragging === DRAG_RIGHT) {
            // Fix the X coordinate.
            this.newBox.x += this.renderContext.percentPerTick
          }
          this.dragging = DRAG_LEFT
        }

        this.newBox.width = (
          eventX -
          this.newBox.x +
          (this.dragging > 0 ? 1 : 0) * this.renderContext.percentPerTick
        )

        this.newBox = canvasAdapter.clip(this.renderContext, this.newBox)
      },
      onMouseUp () {
        if (this.dragging) {
          try {
            let box = this.newBox
            if (box.width < 0) {
              // This is the case if we dragged the note to the left.
              box.width *= -1
              box.x -= box.width
            }
            const note = canvasAdapter.toNote(this.renderContext, box)
            const problematicNotes = this.$store.getters['music/listNotes'].filter((value) => note.disturbs(value))
            if (problematicNotes.length === 0) {
              // there are no problematic notes => we can add a new note
              this.addNoteFromBox(box)
            }
            this.newBox = null
          } catch (e) {
            if (e instanceof NoteTooSmallException) {
            }
          }
        }
        this.dragging = false
        this.newBox = null
      },
      onMouseLeave () {
        this.dragging = false
        this.clicking = false
        this.newBox = null
      }
    }
  }
</script>

<style lang="scss" scoped>
    @import "../../styles/_bootstrap_override.scss";

    .wrapper {
        display: flex;
    }

    .canvas-wrapper {
        position: relative;
        height: 100%;
        width: 100%;
    }
</style>
