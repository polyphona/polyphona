<template>
  <canvas-line v-if="playing" :x="xPos" :vertical="true" :width="3" color="red" :layer="layer"></canvas-line>
</template>

<script>
import Tone from 'tone'
import CanvasLine from './CanvasLine.vue'

export default {
  name: 'progress-bar',
  components: {CanvasLine},
  props: {
    delimiter: {
      type: Object
    },
    layer: {
      type: String
    }
  },
  data () {
    return {
      progress: Tone.Transport.progress,
      interval: null,
      refreshRate: 60
    }
  },
  computed: {
    playing () {
      return this.$store.getters['music/getPlaying']
    },
    xPos () {
      return 100 * this.progress
    }
  },
  methods: {
    getAndStoreProgress () {
      this.progress = Tone.Transport.progress
    }
  },
  watch: {
    // Called everytime `playing` changes.
    playing (nowPlaying) {
      if (nowPlaying) {
        const millis = Math.floor(1000 / this.refreshRate)
        this.interval = setInterval(this.getAndStoreProgress, millis)
      } else if (this.interval) {
        clearInterval(this.interval)
      }
    }
  }
}
</script>
