<template>
    <div class="wrapper">
        <canvas ref="background" class="background"></canvas>
        <canvas ref="foreground" class="foreground"
                @click="onClick"
                @mousedown="onMouseDown"
                @mouseup="onMouseUp"
                @mousemove="onMouseMove"
                @mouseleave="onMouseLeave"
        ></canvas>
        <note-box
                v-if="newBox"
                :x="newBox.x"
                :y="newBox.y"
                :width="newBox.width"
                :height="newBox.height"
                :color="'#afa'"
                layer="foreground"
        ></note-box>
        <note-box
                v-for="box in noteBoxes"
                :key="box.id"
                :x="box.x"
                :y="box.y"
                :width="box.width"
                :height="box.height"
                :color="'#0f0'"
        ></note-box>
    </div>
</template>

<script>
  import {NoteCanvasAdapter} from '@/store/Music'
  import {NoteTooSmallException} from '../../store/Music'
  import NoteBox from './NoteBox'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'NoteCanvas',
    components: {NoteBox},
    data () {
      return {
        newBox: null,
        renderContext: {
          // Percentage of the canvas filled by a quarter note,
          // i.e. 1/4th of a bar.
          percentPerQuarter: 10,
          // Percentage of the canvas filled by a note interval,
          // i.e. the difference in pitch between A and A#
          percentPerInterval: 20
        },
        dragging: false,
        clicking: false,
        canvasDimensions: null,
        layers: {
          background: null,
          foreground: null
        }
      }
    },
    mounted () {
      // Canvas are only accessible once the component is mounted in the DOM
      Object.keys(this.layers).forEach((layer) => this.setUpCanvas(layer))
    },
    provide () {
      // Allow child components to access the layers via `inject: ['layers']`.
      return {
        layers: this.layers
      }
    },
    computed: {
      noteBoxes () {
        return this.$store.getters['MusicStore/listNotes'].map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      }
    },
    methods: {
      setUpCanvas (layer) {
        const canvas = this.$refs[layer]
        this.layers[layer] = canvas.getContext('2d')
        // Store the first layer's parent's dimensions to use the same dimensions
        // for all layers.
        if (!this.canvasDimensions) {
          this.canvasDimensions = {
            width: canvas.parentElement.clientWidth,
            height: canvas.parentElement.clientHeight
          }
        }
        // Resize canvas to fit its parent's width and height
        canvas.width = this.canvasDimensions.width
        canvas.height = this.canvasDimensions.height
      },
      toCanvasPercentPosition (event) {
        // NOTE: canvas layers should have the same size and same top-left position,
        // so it does not matter which layer we choose here
        const canvas = this.$refs['background']
        const canvasLeft = canvas.parentElement.offsetLeft
        const canvasTop = canvas.parentElement.offsetTop
        return {
          x: 100 * (event.pageX - canvasLeft) / canvas.width,
          y: 100 * (event.pageY - canvasTop) / canvas.height
        }
      },
      addNoteFromBox (box) {
        try {
          const note = canvasAdapter.toNote(this.renderContext, box)
          this.$store.dispatch('MusicStore/addNote', note)
          return note
        } catch (e) {
          if (e instanceof NoteTooSmallException) {
            return
          }
          throw e
        }
      },
      onClick (event) {
        if (!this.clicking) {
          return
        }
        let box = {
          ...this.toCanvasPercentPosition(event),
          width: this.renderContext.percentPerQuarter,
          height: this.renderContext.percentPerInterval
        }
        box = canvasAdapter.clip(this.renderContext, box)
        const note = canvasAdapter.toNote(this.renderContext, box)
        const wrappingNotes = this.$store.getters['MusicStore/listNotes'].filter((value) => note.EqualOrcontainedInNote(value))
        if (wrappingNotes.length > 0) { // There is an existing note same as or wrapping the new one : we delete note
          this.$store.dispatch('MusicStore/deleteNote', wrappingNotes[0])
        } else { // there are no problematic notes : we add a new note
          this.addNoteFromBox(box)
        }
        this.clicking = false
      },
      onMouseDown (event) {
        this.clicking = true
        this.dragging = true
        const height = this.renderContext.percentPerInterval
        const width = 0
        const box = {...this.toCanvasPercentPosition(event), width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onMouseMove (event) {
        this.clicking = false
        if (!this.dragging) {
          return
        }
        this.newBox.width = this.toCanvasPercentPosition(event).x - this.newBox.x
        this.newBox = canvasAdapter.clip(this.renderContext, this.newBox)
      },
      onMouseUp (event) {
        this.dragging = false
        let box = this.newBox
        // TODO ajouter bloc try pour toosmallexception
        const note = canvasAdapter.toNote(this.renderContext, box)
        const problematicNotes = this.$store.getters['MusicStore/listNotes'].filter((value) => note.disturbs(value))
        if (problematicNotes.length === 0) { // there are no problematic notes : we add a new note
          this.addNoteFromBox(box)
        }
        this.newBox = null
      },
      onMouseLeave (event) {
        this.dragging = false
        this.clicking = false
        this.newBox = null
      }
    }
  }
</script>

<style lang="scss" scoped>
    .wrapper {
        position: relative;

        .background {
            background: gold;
        }

        .foreground {
            position: absolute;
            top: 0;
            left: 0;
            background: transparent;
        }
    }
</style>
