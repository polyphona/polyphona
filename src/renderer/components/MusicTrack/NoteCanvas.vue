<template>
  <div class="wrapper">
    <canvas ref="note-canvas" @click="onClick"></canvas>
    <!-- Children components will be mounted here -->
    <slot></slot>
  </div>
</template>

<script>
  export default {
    name: 'NoteCanvas',
    data () {
      return {
        provider: {
          context: null
        }
      }
    },
    methods: {
      onClick (event) {
        const canvas = this.$refs['note-canvas']
        const canvasLeft = canvas.offsetLeft
        const canvasTop = canvas.offsetTop
        this.$emit('canvas-click', {
          x: 100 * (event.pageX - canvasLeft) / canvas.width,
          y: 100 * (event.pageY - canvasTop) / canvas.height
        })
      }
    },
    provide () {
      // Allow child components to `inject: ['provider']`
      // and have access to it.
      return {
        provider: this.provider
      }
    },
    mounted () {
      // Canvas is only accessible once the component is mounted in the DOM
      const canvas = this.$refs['note-canvas']
      this.provider.context = canvas.getContext('2d')
      // Resize canvas to fit its parent's width and height
      canvas.width = canvas.parentElement.clientWidth
      canvas.height = canvas.parentElement.clientHeight
    }
  }
</script>

<style lang="scss" scoped>
  .wrapper {
    background: gold;
  }
</style>
