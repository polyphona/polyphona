<template>
  <div id="song-editor">
    <p style="display: flex;">
      <span class="form-field">
        <button @click="togglePlay">{{ playing ? '❙❙' : '►️'}}️</button>
      </span>
      <span class="form-field">
        <label for="octave">Octave:</label>
        <select id="octave" v-model="octave">
          <option :value="1">1</option>
          <option :value="2">2</option>
          <option :value="3">3</option>
          <option :value="4">4</option>
          <option :value="5">5</option>
          <option :value="6">6</option>
        </select>
      </span>
    </p>
    <note-canvas id="note-canvas"></note-canvas>
  </div>
</template>
<script>
  import Tone from 'tone'

  import NoteCanvas from './NoteCanvas.vue'

  export default {
    name: 'song-editor',
    components: {NoteCanvas},
    data () {
      return {
        newBox: null,
        playing: false,
        synth: new Tone.PluckSynth().toMaster(),
        octave: 4
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
        const quarter = Math.floor(canvasTime / this.musicContext.division)
        const sixteenth = 4 / this.musicContext.division * (canvasTime % this.musicContext.division)
        return `0:${quarter}:${sixteenth}`
      },
      _play (offset) {
        // Notation: "bar:quarter:sixteenth"
        // See: https://github.com/Tonejs/Tone.js/wiki/Time#transport-time
        this.track.notes.forEach((note) => {
          const trigger = (time) => {
            const pitch = this.musicContext.scale[note.pitch] + this.octave
            this.synth.triggerAttackRelease(pitch, this._toTransportTime(note.duration), time)
          }
          Tone.Transport.schedule(trigger, this._toTransportTime(note.startTime))
        })
        // Loop one measure
        Tone.Transport.loopEnd = '1m'
        Tone.Transport.loop = true
        Tone.Transport.start(Tone.Transport.now(), offset)
      }
    },
    computed: {
      track () {
        return this.$store.getters['MusicStore/getTrack']
      },
      musicContext () {
        return this.$store.getters['MusicStore/getMusicContext']
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

  .form-field {
    margin: 1em;
  }
</style>
