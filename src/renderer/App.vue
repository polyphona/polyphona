<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue'
  export default {
    name: 'polyphona',
    components: { 'nav-bar': Navbar }
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
