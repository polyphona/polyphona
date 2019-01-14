<script>
  /*
  NOTE: NoteBox is not a "real" Vue component; it has no template nor styles, so it does
  not render to the DOM.
  Instead, it provides a render() function directly which draws the note box to the canvas.
   */

  // Helper functions to convert a percentage of canvas area to pixels.
  const percentWidthToPix = (percent, ctx) => Math.floor((ctx.canvas.width / 100) * percent)
  const percentHeightToPix = (percent, ctx) => Math.floor((ctx.canvas.height / 100) * percent)

  export default {
    inject: ['layers'],
    props: {
      // Top-left corner coordinates (percentage of canvas dimensions)
      x: {
        type: Number,
        default: 0
      },
      y: {
        type: Number,
        default: 0
      },
      // Width and height (percentage of canvas dimensions)
      width: {
        type: Number,
        default: 0
      },
      height: {
        type: Number,
        default: 0
      },
      // Color of the box
      color: {
        type: String,
        default: '#f00'
      },
      layer: {
        type: String,
        default: 'background'
      }
    },
    data () {
      return {
        strokeWidth: 10,
        oldBox: {
          x: 0,
          y: 0,
          width: 0,
          height: 0
        }
      }
    },
    computed: {
      context () {
        return this.layers[this.layer]
      },
      calculatedBox () {
        const ctx = this.context
        const box = {
          x: percentWidthToPix(this.x, ctx),
          y: percentHeightToPix(this.y, ctx),
          width: percentWidthToPix(this.width, ctx),
          height: percentHeightToPix(this.height, ctx)
        }
        this.oldBox = box
        return box
      }
    },
    methods: {
      onClick () {
        this.$emit('box-click', {
          box: this.calculatedBox()
        })
      },
      clearOldBox: function (ctx) {
        const oldBox = this.oldBox
        ctx.clearRect(oldBox.x, oldBox.y, oldBox.width, oldBox.height)
      }
    },
    render () {
      const ctx = this.context

      // It is *possible* that the canvas context may not be injected yet
      if (!ctx) {
        return
      }

      ctx.beginPath()
      this.clearOldBox(ctx)

      const newBox = this.calculatedBox

      if (!newBox.width) {
        return
      }
      // Draw the new box
      ctx.rect(
        newBox.x,
        newBox.y,
        newBox.width,
        newBox.height
      )
      ctx.save()
      ctx.clip()
      ctx.fillStyle = this.color
      ctx.lineWidth = this.strokeWidth
      ctx.fill()
      ctx.stroke()
      ctx.restore()
    },
    destroyed () {
      // When note component is destroyed, un-draw it from the canvas
      const ctx = this.context
      this.clearOldBox(ctx)
    }
  }
</script>
