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
  export default {
    name: 'NoteCanvas',
    data () {
      return {
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
      onClick (event) {
        if (!this.clicking) {
          return
        }
        this.$emit('canvas-click', this.toCanvasPercentPosition(event))
        this.clicking = false
      },
      onMouseDown (event) {
        this.clicking = true
        this.dragging = true
        this.$emit('canvas-mousedown', this.toCanvasPercentPosition(event))
      },
      onMouseMove (event) {
        this.clicking = false
        if (!this.dragging) {
          return
        }
        this.$emit('canvas-mousedrag', this.toCanvasPercentPosition(event))
      },
      onMouseUp (event) {
        this.dragging = false
        this.$emit('canvas-mouseup', this.toCanvasPercentPosition(event))
      },
      onMouseLeave (event) {
        this.dragging = false
        this.clicking = false
        this.$emit('canvas-mouseleave', this.toCanvasPercentPosition(event))
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
