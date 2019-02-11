<template>
  <nav>
    <h1 id="brand">
      <router-link to="/">♫ Polyphona</router-link>
    </h1>
    <ul>
      <li v-if="user" id="display-username">👤
        <strong>{{user.username}}</strong>
      </li>
      <li v-if="user">
        <button class="btn btn-light" @click="logout">Log out</button>
      </li>
      <li v-if="!loggedIn">
        <router-link class="btn" to="login">Sign in</router-link>
      </li>
      <li v-if="!loggedIn">
        <router-link class="btn btn-primary" to="register">Sign up</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'nav-bar',
  computed: {
    user () {
      return this.$store.getters['auth/getUser']
    },
    loggedIn () {
      return !!this.user
    }
  },
  methods: {
    logout () {
      return this.$store.dispatch('auth/logout')
    }
  }
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
    align-items: center;
  }
  #display-username {
    margin-right: 1em;
  }
}
</style>
