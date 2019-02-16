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
  @import './styles/_bootstrap_override.scss';

  html, body {
    // Use the entire viewport width and height.
    width: 100vw;
    height: 100vh;
  }
  #app {
    width: 100%;
    height: 100%;
  }
</style>
