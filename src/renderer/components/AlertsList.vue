<template>
  <ul>
    <li
      v-for="alert in alerts"
      :key="alert.id"
      class="alert alert-dismissable fade show"
      :class="['alert-' + alert.kind]"
      role="alert"
    >
      {{ alert.message }}
      <button
        type="button"
        class="close"
        @click="removeAlert(alert)"
        aria-label="Close"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'alerts-list',
  computed: {
    alerts () {
      return this.$store.getters['alerts/list']
    }
  },
  methods: {
    removeAlert (alert) {
      this.$store.dispatch('alerts/remove', alert.id)
    }
  }
}
</script>

<style lang="scss" scoped>
  ul {
      list-style-type: none;
      margin: 0;
      padding: 0 .5em;
  }
</style>
