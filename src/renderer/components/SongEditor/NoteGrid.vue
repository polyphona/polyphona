<template>
  <div>
    <canvas-line
      v-for="delimiter in delimiters"
      :x="delimiter.x"
      :y="delimiter.y"
      :vertical="delimiter.vertical"
      :width="delimiter.width"
      :key="'delimiter-' + delimiter.id"
      :layer="layer"
    ></canvas-line>
  </div>
</template>

<script>
import CanvasLine from './CanvasLine.vue'

export default {
  name: 'note-grid',
  components: {CanvasLine},
  props: {
    layer: {
      type: String
    }
  },
  data () {
    return {
      // For `:key` on delimiters
      delimiterId: 0
    }
  },
  computed: {
    musicContext () {
      return this.$store.getters['music/getMusicContext']
    },
    renderContext () {
      return this.$store.getters['music/getRenderContext']
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
    }
  }
}
</script>
