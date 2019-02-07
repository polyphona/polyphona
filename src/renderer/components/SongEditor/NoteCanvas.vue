<template>
  <div class="wrapper">
    <!-- Show the names of the notes in a column. -->
    <ol id="note-pitches">
      <li v-for="pitch in pitches" :key="'pitch-' + pitch.id">{{ pitch.name }}</li>
    </ol>
    <div class="canvas-wrapper">
      <!-- Canvas layers. -->
      <canvas ref="background" class="background"></canvas>
      <canvas ref="notes" class="layer"></canvas>
      <canvas
        ref="foreground"
        class="layer"
        @click="onClick"
        @mousedown="onMouseDown"
        @mouseup="onMouseUp"
        @mousemove="onMouseMove"
        @mouseleave="onMouseLeave"
      ></canvas>

      <!-- Delimiters of notes on the canvas -->
      <canvas-delimiter
        v-for="delimiter in delimiters"
        :x="delimiter.x"
        :y="delimiter.y"
        :vertical="delimiter.vertical"
        :width="delimiter.width"
        :key="'delimiter-' + delimiter.id"
        layer="background"
      ></canvas-delimiter>

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
        :key="'note-' + box.id"
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
  import {NoteCanvasAdapter, SCALE, NoteTooSmallException} from '@/store/Music'
  import NoteBox from './NoteBox'
  import CanvasDelimiter from './CanvasDelimiter.vue'

  const canvasAdapter = new NoteCanvasAdapter()

  const DRAG_RIGHT = 1
  const DRAG_NONE = 0
  const DRAG_LEFT = -1

  export default {
    name: 'NoteCanvas',
    components: {NoteBox, CanvasDelimiter},
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
          foreground: null
        },
        delimiterId: 0
      }
    },
    mounted () {
      // Canvas are only accessible once the component is mounted in the DOM
      Object.keys(this.layers).forEach((layer) => this.setUpCanvas(layer))
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
      musicContext () {
        return this.$store.getters['MusicStore/getMusicContext']
      },
      renderContext () {
        return this.$store.getters['MusicStore/getRenderContext']
      },
      delimiters () {
        const division = this.musicContext.division
        const stepX = this.renderContext.percentPerTick
        const stepY = this.renderContext.percentPerInterval
        const verticalDelimiters = []
        for (let i = 0; i < 100 / stepX; i++) {
          verticalDelimiters.push({
            id: this.delimiterId,
            x: stepX * i,
            vertical: true,
            width: i % division === 0 ? 4 : 1
          })
          this.delimiterId++
        }
        const horizontalDelimiters = []
        for (let i = 0; i < 100 / stepY; i++) {
          horizontalDelimiters.push({
            id: this.delimiterId,
            y: stepY * i,
            vertical: false
          })
          this.delimiterId++
        }
        return [...horizontalDelimiters, ...verticalDelimiters]
      },
      pitches () {
        return Object.keys(SCALE).map((index) => ({
          id: index,
          name: SCALE[index]
        })).reverse()
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
        const canvas = this.$refs['background']
        const canvasLeft = canvas.parentElement.offsetLeft
        const canvasTop = canvas.parentElement.offsetTop
        return {
          x: 100 * (event.pageX - canvasLeft) / canvas.width,
          y: 100 * (event.pageY - canvasTop) / canvas.height
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
        const collidingNotes = this.$store.getters['MusicStore/listNotes'].filter((value) => note.collides(value))
        if (collidingNotes.length > 0) {
          collidingNotes.forEach((note) => this.$store.dispatch('MusicStore/deleteNote', note))
        } else {
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
          this.addNoteFromBox(this.newBox)
        }
        this.dragging = false
        this.newBox = null
      },
      onMouseLeave (event) {
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
    // position: relative;
    display: flex;
  }
  #note-pitches {
    display: flex;
    flex-flow: column;
    list-style-type: none;
    padding: 0;
    margin: 0;
    text-align: center;
    color: map-get($theme-colors, "light");
    background: map-get($theme-colors, "dark");
    li {
      padding: 0 .5em;
      margin: auto 0;
    }
  }
  .canvas-wrapper {
    position: relative;
    height: 100%;
    flex: 1;

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
