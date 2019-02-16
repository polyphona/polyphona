<template>
  <div ref="container">
    <canvas v-for="name in names" :key="name" :ref="name" class="layer"></canvas>
    <slot>
      <!--
      Child components will get rendered here.
      See: https://fr.vuejs.org/v2/guide/components-slots.html
      -->
    </slot>
  </div>
</template>

<script>
import {MouseCanvasAdapter} from './adapters'

const mouseAdapter = new MouseCanvasAdapter()

export default {
  name: 'canvas-layers',
  props: {
    names: {
      type: Array
    }
  },
  data () {
    const layers = {}
    this.names.forEach((name) => {
      layers[name] = null
    })

    return {
      layers,
      // Events that should be listened to on the top-most canvas.
      events: ['click', 'mousemove', 'mousedown', 'mouseup', 'mouveleave'],
      // Dimensions of the canvas (and each layer by extension).
      dimensions: null
    }
  },
  provide () {
    // Allow child components to access the layers via `inject: ['layers']`.
    return {
      layers: this.layers
    }
  },
  mounted () {
    // Canvases are only accessible once the component is mounted in the DOM.
    this.names.forEach((name) => this.setUpCanvas(name))
    // Listen to window resize events to resize the canvases accordingly.
    window.addEventListener('resize', this.onWindowResize)
    this.listenToEvents()
  },
  destroyed () {
    window.removeEventListener('resize', this.onWindowResize)
  },
  methods: {
    listenToEvents () {
      /*
      NOTE:
      - Events on the container are not propagated to
      the parent component (possibly because of an issue with slots),
      e.g. if we don't manually bind them, the parent component cannot use
      `@click` or `@mousemove`.
      - We bind the events programmatically because it would be repetitive
      to do position conversion and re-emission on the container directly.
      */
      const container = this.$refs.container
      this.events.forEach((event) => {
        container['on' + event] = (e) => {
          this.$emit(event, this.toCanvasPercentPosition(e))
        }
      })
    },
    toCanvasPercentPosition (event) {
      // NOTE: canvas layers have the same size and same top-left position
      // by construction, so it does not matter which layer we choose here.
      const ctx = this.layers[this.names[0]]
      const canvasLeft = ctx.canvas.parentElement.offsetLeft
      const canvasTop = ctx.canvas.parentElement.offsetTop
      return {
        x: mouseAdapter.pixWidthToPercent(event.pageX - canvasLeft, ctx),
        y: mouseAdapter.pixHeightToPercent(event.pageY - canvasTop, ctx)
      }
    },
    setUpCanvas (name) {
      const canvas = this.$refs[name][0]
      this.layers[name] = canvas.getContext('2d')
      // Store the first layer's parent's dimensions to use the same dimensions
      // for all layers.
      if (!this.dimensions) {
        this.dimensions = {
          width: canvas.parentElement.clientWidth,
          height: canvas.parentElement.clientHeight
        }
      }
      // Resize canvas to fit its parent's width and height
      canvas.width = this.dimensions.width
      canvas.height = this.dimensions.height
    },
    onWindowResize () {
      const container = this.$refs['container']
      // Update each layer's width and height to match that of the container.
      Object.values(this.layers).forEach(({canvas}) => {
        canvas.width = container.clientWidth
        canvas.height = container.clientHeight
      })
      this.$emit('resized')
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../../styles/_bootstrap_override.scss";

.background {
  background: map-get($theme-colors, "light");
}

.layer {
  position: absolute;
  top: 0;
  left: 0;
  background: transparent;
}
</style>
