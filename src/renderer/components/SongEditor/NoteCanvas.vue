<template>
  <div class="wrapper">
    <pitch-header></pitch-header>

    <div ref="canvas-container" class="canvas-wrapper">
      <!-- Canvas layers. -->
      <canvas ref="background" class="background"></canvas>
      <canvas ref="notes" class="layer"></canvas>
      <canvas ref="decorations" class="layer"></canvas>
      <canvas
        ref="foreground"
        class="layer"
        @click="onClick"
        @mousedown="onMouseDown"
        @mouseup="onMouseUp"
        @mousemove="onMouseMove"
        @mouseleave="onMouseLeave"
      ></canvas>

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
    </div>
  </div>
</template>

<script>
  import {NoteCanvasAdapter, MouseCanvasAdapter} from './adapters'
  import {NoteTooSmallException} from './errors'
  import NoteBox from './NoteBox'
  import CanvasLine from './CanvasLine.vue'
  import ProgressBar from './ProgressBar.vue'
  import NoteGrid from './NoteGrid.vue'
  import PitchHeader from './PitchHeader.vue'

  const mouseAdapter = new MouseCanvasAdapter()
  const canvasAdapter = new NoteCanvasAdapter()

  const DRAG_RIGHT = 1
  const DRAG_NONE = 0
  const DRAG_LEFT = -1

  export default {
    name: 'NoteCanvas',
    components: {NoteBox, CanvasLine, ProgressBar, NoteGrid, PitchHeader},
    data () {
      return {
        newBox: null,
        // Determines whether we're dragging a new note,
        // and in which direction.
        dragging: false,
        clicking: false,
        canvasDimensions: null,
        layers: {
          background: null,
          notes: null,
          decorations: null,
          foreground: null
        },
        // Gets incremented when the canvas needs to be re-rendered.
        // This is why we use it in the canvas components' `:key`.
        canvasId: 0
      }
    },
    mounted () {
      // Canvas are only accessible once the component is mounted in the DOM
      Object.keys(this.layers).forEach((layer) => this.setUpCanvas(layer))
      // Listen to window resize events to resize the canvases accordingly.
      window.addEventListener('resize', this.onWindowResize)
    },
    provide () {
      // Allow child components to access the layers via `inject: ['layers']`.
      return {
        layers: this.layers
      }
    },
    computed: {
      noteBoxes () {
        return this.$store.getters['MusicStore/listNotes'].map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      },
      renderContext () {
        return this.$store.getters['MusicStore/getRenderContext']
      }
    },
    methods: {
      setUpCanvas (layer) {
        const canvas = this.$refs[layer]
        this.layers[layer] = canvas.getContext('2d')
        // Store the first layer's parent's dimensions to use the same dimensions
        // for all layers.
        if (!this.canvasDimensions) {
          this.canvasDimensions = {
            width: canvas.parentElement.clientWidth,
            height: canvas.parentElement.clientHeight
          }
        }
        // Resize canvas to fit its parent's width and height
        canvas.width = this.canvasDimensions.width
        canvas.height = this.canvasDimensions.height
      },
      toCanvasPercentPosition (event) {
        // NOTE: canvas layers should have the same size and same top-left position,
        // so it does not matter which layer we choose here
        const ctx = this.layers.background
        const canvasLeft = ctx.canvas.parentElement.offsetLeft
        const canvasTop = ctx.canvas.parentElement.offsetTop
        return {
          x: mouseAdapter.pixWidthToPercent(event.pageX - canvasLeft, ctx),
          y: mouseAdapter.pixHeightToPercent(event.pageY - canvasTop, ctx)
        }
      },
      addNoteFromBox (box) {
        try {
          const note = canvasAdapter.toNote(this.renderContext, box)
          this.$store.dispatch('MusicStore/addNote', note)
          return note
        } catch (e) {
          if (e instanceof NoteTooSmallException) {
            return
          }
          throw e
        }
      },
      onClick (event) {
        if (!this.clicking) {
          return
        }
        let box = {
          ...this.toCanvasPercentPosition(event),
          width: this.renderContext.percentPerTick,
          height: this.renderContext.percentPerInterval
        }
        box = canvasAdapter.clip(this.renderContext, box)
        const note = canvasAdapter.toNote(this.renderContext, box)
        const existingNote = this.$store.getters['MusicStore/listNotes'].filter((value) => note.disturbs(value))
        if (existingNote.length > 0) { // There is an existing note : we delete note
          this.$store.dispatch('MusicStore/deleteNote', existingNote[0])
        } else { // there are no problematic notes : we add a new note
          this.addNoteFromBox(box)
        }
        this.clicking = false
      },
      onMouseDown (event) {
        this.clicking = true
        this.dragging = DRAG_NONE
        const height = this.renderContext.percentPerInterval
        const width = this.renderContext.percentPerTick
        const box = {...this.toCanvasPercentPosition(event), width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onMouseMove (event) {
        this.clicking = false
        if (this.dragging === false) {
          return
        }

        const eventX = this.toCanvasPercentPosition(event).x
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
      onMouseUp (event) {
        if (this.dragging) {
          try {
            let box = this.newBox
            if (box.width < 0) {
              // This is the case if we dragged the note to the left.
              box.width *= -1
              box.x -= box.width
            }
            const note = canvasAdapter.toNote(this.renderContext, box)
            const problematicNotes = this.$store.getters['MusicStore/listNotes'].filter((value) => note.disturbs(value))
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
      onMouseLeave (event) {
        this.dragging = false
        this.clicking = false
        this.newBox = null
      },
      onWindowResize () {
        const container = this.$refs['canvas-container']
        // Update each layer's width and height to match that of the container.
        Object.values(this.layers).forEach((ctx) => {
          ctx.canvas.width = container.clientWidth
          ctx.canvas.height = container.clientHeight
        })
        // Increment the canvas ID so that components that use it in
        // their `:key` get re-rendered by Vue.
        this.canvasId++
      }
    },
    destroyed () {
      window.removeEventListener('resize', this.onWindowResize)
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

        .background {
            background: map-get($theme-colors, "light");
        }

        .layer {
            position: absolute;
            top: 0;
            left: 0;
            background: transparent;
        }
    }
</style>
