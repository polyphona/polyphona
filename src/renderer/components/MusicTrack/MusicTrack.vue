<template>
  <div>
    <table class="table table-bordered">
      <tbody>
      <tr>
        <cell v-for="(cell, index) in track.getCellList()" :key="index" :id="index" :cell="cell" @switch-cell-state="switchCellState"></cell>
      </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
  import Cell from './Cell.vue'
  import Track from './Music.js'

  export default {
    name: 'custom-track',
    components: {Cell},
    data () {
      return {
        track: new Track(4, 1)
      }
    },
    methods: {
      switchCellState (input) {
        if (input.cell.activated) {
          this.track.addNote(input.id)
        }
      }
    }
  }
</script>
<style>
</style>
