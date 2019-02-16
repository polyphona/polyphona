<script>
  /* NOTE: this is a JS-only component. */
  import { percentWidthToPix, percentHeightToPix } from './utils'

  export default {
    inject: ['layers'],
    props: {
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
    data () {
      return {
        box: null
      }
    },
    computed: {
      context () {
        const ctx = this.layers[this.layer]
        return ctx
      },
      line () {
        const ctx = this.context
        const line = {
          start: {
            x: percentWidthToPix(this.vertical ? this.x : 0, ctx),
            y: percentHeightToPix(this.vertical ? 0 : this.y, ctx)
          },
          end: {
            x: percentWidthToPix(this.vertical ? this.x : 100, ctx),
            y: percentHeightToPix(this.vertical ? 100 : this.y, ctx)
          }
        }
        // NOTE: this only works for vertical lines.
        this.box = {
          x: line.start.x - this.width,
          y: line.start.y,
          width: 2 * this.width,
          height: line.end.y - line.start.y
        }
        return line
      }
    },
    methods: {
      clear (ctx) {
        const box = this.box
        if (!box) {
          return
        }
        ctx.clearRect(box.x, box.y, box.width, box.height)
      }
    },
    render () {
      const ctx = this.context

      // It is *possible* that the canvas context may not be injected yet.
      if (!ctx) {
        return
      }

      this.clear(ctx)
      const {start, end} = this.line

      ctx.beginPath()
      ctx.save()
      ctx.moveTo(start.x, start.y)
      ctx.lineTo(end.x, end.y)
      ctx.strokeStyle = this.color
      ctx.lineWidth = this.width
      ctx.stroke()
      ctx.restore()
    },
    destroyed () {
      this.clear(this.context)
    }
  }
</script>
