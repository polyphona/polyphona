<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'polyphona'
  }
</script>

<style lang="scss">
  @import "../../node_modules/bootstrap/scss/bootstrap.scss";
  html, body {
    width: 100vw;
    height: 100vh;
  }
  #app {
    width: 100%;
    height: 100%;
  }
</style>
