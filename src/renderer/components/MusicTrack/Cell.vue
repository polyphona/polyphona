<template>
  <td class="cell" v-bind:class="{'table-primary': localCell.activated}" @click="switchState">
  </td>
</template>

<script>
  export default {
    name: 'Cell',
    props: {
      id: Number,
      cell: Object
    },
    data () {
      return {
        localCell: this.cell
      }
    },
    methods: {
      switchState () {
        this.localCell.activated = !this.localCell.activated
        this.$emit('switch-cell-state', {cell: this.localCell, id: this.id})
      }
    }
  }
</script>

<style scoped>

</style>
