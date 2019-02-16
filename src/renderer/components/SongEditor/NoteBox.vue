<script>
  /*
  NOTE: NoteBox is not a "real" Vue component; it has no template
  nor styles, so it does not render to the DOM.
  Instead, it provides a render() function directly which draws the
  note box to the canvas.
  */

  import {Box, MouseCanvasAdapter} from '@/models'

  const adapter = new MouseCanvasAdapter()

  export default {
    inject: ['layers'],
    props: {
      box: {
        // See: models/note.js
        type: Object
      },
      // Color of the box
      color: {
        type: String,
        default: '#f6cd4c'
      },
      layer: {
        type: String,
        default: 'background'
      }
    },
    data () {
      return {
        strokeWidth: 1,
        oldBox: new Box({
          x: 0,
          y: 0,
          width: 0,
          height: 0
        })
      }
    },
    computed: {
      context () {
        return this.layers[this.layer]
      },
      calculatedBox () {
        const ctx = this.context
        const box = new Box({
          x: adapter.percentWidthToPix(this.box.x, ctx),
          y: adapter.percentHeightToPix(this.box.y, ctx),
          width: adapter.percentWidthToPix(this.box.width, ctx),
          height: adapter.percentHeightToPix(this.box.height, ctx)
        })
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
      ctx.strokeStyle = '#999'
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
