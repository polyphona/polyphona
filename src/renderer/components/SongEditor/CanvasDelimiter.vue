<script>
  /* NOTE: this is a JS-only component. */
  import { percentWidthToPix, percentHeightToPix } from './utils'

  export default {
    inject: ['layers'],
    props: {
      // X coordinate (percentage of canvas dimensions)
      x: {
        type: Number,
        default: 0
      },
      y: {
        type: Number,
        default: 0
      },
      vertical: {
        type: Boolean,
        default: true
      },
      width: {
        type: Number,
        default: 1
      },
      color: {
        type: String,
        default: '#ddd'
      },
      layer: {
        type: String
      }
    },
    computed: {
      context () {
        return this.layers[this.layer]
      },
      line () {
        return {
          start: {
            x: percentWidthToPix(this.vertical ? this.x : 0, this.context),
            y: percentHeightToPix(this.vertical ? 0 : this.y, this.context)
          },
          end: {
            x: percentWidthToPix(this.vertical ? this.x : 100, this.context),
            y: percentHeightToPix(this.vertical ? 100 : this.y, this.context)
          }
        }
      }
    },
    render () {
      const ctx = this.context

      // It is *possible* that the canvas context may not be injected yet.
      if (!ctx) {
        return
      }

      const {start, end} = this.line

      ctx.beginPath()
      ctx.save()
      ctx.moveTo(start.x, start.y)
      ctx.lineTo(end.x, end.y)
      ctx.strokeStyle = this.color
      ctx.lineWidth = this.width
      ctx.stroke()
      ctx.restore()
    }
  }
</script>
