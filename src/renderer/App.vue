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
  @import "../../node_modules/bootstrap/scss/bootstrap.scss";
  @import url('https://fonts.googleapis.com/css?family=Amatic+SC');

  $font-family-titles: "Amatic SC", cursive;

  html, body {
    width: 100vw;
    height: 100vh;
  }
  h1, h2, h3, h4, h5, h6 {
    font-family: $font-family-titles;
  }
  #app {
    width: 100%;
    height: 100%;
  }
</style>
