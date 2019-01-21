<template>
  <div class="wrapper">
    <canvas ref="background" class="background"></canvas>
    <canvas ref="foreground" class="foreground"
            @click="onClick"
            @mousedown="onMouseDown"
            @mouseup="onMouseUp"
            @mousemove="onMouseMove"
            @mouseleave="onMouseLeave"
    ></canvas>
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
  </div>
</template>

<script>
  import {NoteCanvasAdapter, NoteTooSmallException} from '@/store/Music'
  import NoteBox from './NoteBox'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'NoteCanvas',
    components: {NoteBox},
    data () {
      return {
        newBox: null,
        dragging: false,
        clicking: false,
        canvasDimensions: null,
        layers: {
          background: null,
          foreground: null
        }
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
        this.dragging = true
        const height = this.renderContext.percentPerInterval
        const width = 0
        const box = {...this.toCanvasPercentPosition(event), width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onMouseMove (event) {
        this.clicking = false
        if (!this.dragging) {
          return
        }
        this.newBox.width = this.toCanvasPercentPosition(event).x - this.newBox.x
        this.newBox = canvasAdapter.clip(this.renderContext, this.newBox)
      },
      onMouseUp (event) {
        this.dragging = false
        this.addNoteFromBox(this.newBox)
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
  .wrapper {
    position: relative;

    .background {
      background: gold;
    }

    .foreground {
      position: absolute;
      top: 0;
      left: 0;
      background: transparent;
    }
  }
</style>
