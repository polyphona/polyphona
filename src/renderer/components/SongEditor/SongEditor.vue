<template>
  <div id="song-editor">
    <p style="display: flex;">
      <button @click="togglePlay">{{ playing ? '❙❙' : '►️'}}️</button>
      <select v-model="octave">
        <option :value="1">1</option>
        <option :value="2">2</option>
        <option :value="3">3</option>
        <option :value="4">4</option>
        <option :value="5">5</option>
        <option :value="6">6</option>
      </select>
    </p>
    <note-canvas
      id="note-canvas"
      @canvas-click="onCanvasClick"
      @canvas-mousedown="onCanvasMouseDown"
      @canvas-mousedrag="onCanvasMouseDrag"
      @canvas-mouseup="onCanvasMouseUp"
      @canvas-mouseleave="onCanvasMouseLeave">
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
        :x="box.x"
        :y="box.y"
        :width="box.width"
        :height="box.height"
        :color="'#0f0'"
      ></note-box>
    </note-canvas>
  </div>
</template>
<script>
  import {Track, NoteCanvasAdapter, NoteTooSmallException} from './Music.js'
  import NoteCanvas from './NoteCanvas.vue'
  import NoteBox from './NoteBox.vue'
  import Tone from 'tone'

  const canvasAdapter = new NoteCanvasAdapter()

  export default {
    name: 'song-editor',
    components: {NoteCanvas, NoteBox},
    data () {
      const track = new Track()
      const division = 4
      return {
        track,
        newBox: null,
        playing: false,
        synth: new Tone.MonoSynth().toMaster(),
        octave: 4,
        division,
        renderContext: {
          // Percentage of the canvas filled by one tick, from 0 to 100.
          percentPerTick: 100 / (4 * division),
          // Percentage of the canvas filled by a note interval, from 0 to 100
          percentPerInterval: 100 / 12
        },
        scale: {
          0: 'C',
          1: 'C#',
          2: 'D',
          3: 'D#',
          4: 'E',
          5: 'F',
          6: 'F#',
          7: 'G',
          8: 'G#',
          9: 'A',
          10: 'A#',
          11: 'B',
          12: 'C'
        }
      }
    },
    mounted () {
      Tone.Transport.bpm.value = 120
    },
    methods: {
      togglePlay () {
        if (this.playing) {
          Tone.Transport.stop()
        } else {
          this._play()
        }
        this.playing = !this.playing
      },
      _toTransportTime (canvasTime) {
        const quarter = Math.floor(canvasTime / this.division)
        const sixteenth = 4 / this.division * (canvasTime % this.division)
        return `0:${quarter}:${sixteenth}`
      },
      _play (offset) {
        // Notation: "bar:quarter:sixteenth"
        // See: https://github.com/Tonejs/Tone.js/wiki/Time#transport-time
        this.track.notes.forEach((note) => {
          const trigger = (time) => {
            const pitch = this.scale[note.pitch] + this.octave
            this.synth.triggerAttackRelease(pitch, this._toTransportTime(note.duration), time)
          }
          Tone.Transport.schedule(trigger, this._toTransportTime(note.startTime))
        })
        // Loop one measure
        Tone.Transport.loopEnd = '1m'
        Tone.Transport.loop = true
        Tone.Transport.start(Tone.Transport.now(), offset)
      },
      addNoteFromBox (box) {
        try {
          const note = canvasAdapter.toNote(this.renderContext, box)
          this.track.addNote(note)
          if (this.playing) {
            // Restart Tone transport timeline
            const elapsed = Tone.Transport.getSecondsAtTime()
            Tone.Transport.stop()
            this._play(elapsed)
          }
          return note
        } catch (e) {
          if (e instanceof NoteTooSmallException) {
            return
          }
          throw e
        }
      },
      onCanvasClick ({x, y}) {
        let box = {
          x,
          y,
          width: this.renderContext.percentPerTick,
          height: this.renderContext.percentPerInterval
        }
        box = canvasAdapter.clip(this.renderContext, box)
        this.addNoteFromBox(box)
      },
      onCanvasMouseDown ({x, y}) {
        const height = this.renderContext.percentPerInterval
        const width = this.renderContext.percentPerTick
        const box = {x, y, width, height}
        this.newBox = canvasAdapter.clip(this.renderContext, box)
      },
      onCanvasMouseDrag ({x, y}) {
        this.newBox.width = x - this.newBox.x + this.renderContext.percentPerTick
        this.newBox.y = y
        this.newBox = canvasAdapter.clip(this.renderContext, this.newBox)
      },
      onCanvasMouseUp () {
        this.addNoteFromBox(this.newBox)
        this.newBox = null
      },
      onCanvasMouseLeave () {
        this.newBox = null
      }
    },
    computed: {
      noteBoxes () {
        return this.track.notes.map(
          (note) => canvasAdapter.toBox(this.renderContext, note)
        )
      }
    }
  }
</script>
<style lang="scss" scoped>
  #song-editor {
    height: 70%;
  }

  #note-canvas {
    width: 100%;
    height: 100%;
  }
</style>
