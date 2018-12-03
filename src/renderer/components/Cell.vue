<template>
    <td class="cell" v-bind:class="{'table-primary': noteState}" @click="switchState">
    </td>
</template>

<script>
  export default {
    name: 'Cell',
    data () {
      return {
        noteState: false
      }
    },
    methods: {
      switchState () {
        this.noteState = !this.noteState
      }
    }
  }
</script>

<style scoped>

</style>
