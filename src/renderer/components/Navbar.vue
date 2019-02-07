<template>
  <nav>
    <h1 id="brand">
      <router-link to="/">♫ Polyphona</router-link>
    </h1>
    <ul>
      <li>
        <router-link class="btn" to="login">Sign in</router-link>
      </li>
      <li>
        <router-link class="btn btn-primary" to="register">Sign up</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'nav-bar'
}
</script>

<style lang="scss" scoped>
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: .5em 1em;
  #brand {
    margin: 0;
    padding: 0;
  }
  ul {
    display: flex;
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
}
</style>
