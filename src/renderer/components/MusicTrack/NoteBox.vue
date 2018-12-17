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
    inject: ['provider'],
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
      }
    },
    data () {
      return {
        oldBox: {
          x: 0,
          y: 0,
          width: 0,
          height: 0
        }
      }
    },
    computed: {
      calculatedBox () {
        const ctx = this.provider.context
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
    render () {
      // It is *possible* that the canvas context may not be injected yet
      if (!this.provider.context) {
        return
      }
      const ctx = this.provider.context
      ctx.beginPath()

      const oldBox = this.oldBox
      const newBox = this.calculatedBox

      // Clear old box
      ctx.clearRect(oldBox.x, oldBox.y, oldBox.width, oldBox.height)

      // Draw the new box
      ctx.rect(newBox.x, newBox.y, newBox.width, newBox.height)
      ctx.fillStyle = this.color
      ctx.fill()
      ctx.stroke()
    }
  }
</script>
