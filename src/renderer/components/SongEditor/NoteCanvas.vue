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
    <!-- Children components will be mounted here -->
    <slot></slot>
  </div>
</template>

<script>
  import {NoteCanvasAdapter} from '@/store/Music'
  import {NoteTooSmallException} from '../../store/Music'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'NoteCanvas',
    data () {
      return {
        newBox: null,
        renderContext: {
          // Percentage of the canvas filled by a quarter note,
          // i.e. 1/4th of a bar.
          percentPerQuarter: 10,
          // Percentage of the canvas filled by a note interval,
          // i.e. the difference in pitch between A and A#
          percentPerInterval: 20
        },
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
          width: this.renderContext.percentPerQuarter,
          height: this.renderContext.percentPerInterval
        }
        box = canvasAdapter.clip(this.renderContext, box)
        this.addNoteFromBox(box)
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
