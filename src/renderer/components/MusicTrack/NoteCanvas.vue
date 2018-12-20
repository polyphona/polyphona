<template>
  <div class="wrapper">
    <canvas ref="note-canvas" @click="onClick"></canvas>
    <!-- Children components will be mounted here -->
    <slot></slot>
  </div>
</template>

<script>
  import {mapActions} from 'vuex'
  import {NoteCanvasAdapter} from '@/store/Music'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'NoteCanvas',
    data () {
      return {
        provider: {
          context: null
        },
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
    methods: Object.assign({
      onClick (event) {
        const canvas = this.$refs['note-canvas']
        const canvasLeft = canvas.offsetLeft
        const canvasTop = canvas.offsetTop
        const x = 100 * (event.pageX - canvasLeft) / canvas.width
        const y = 100 * (event.pageY - canvasTop) / canvas.height
        const box = {x, y, width: 10, height: 10}
        const note = canvasAdapter.toNote(this.renderContext, box)
        this.addNote(note)
      }
    }, mapActions(['addNote'])),
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
