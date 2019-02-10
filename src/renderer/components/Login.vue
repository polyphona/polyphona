<template>
  <div class="container" id="container">
    <h1>Sign in</h1>
    <p class="text-muted">Enter your Polyphona account details to sign in.</p>

    <div class="alert alert-danger" v-if="error" role="alert">{{ error }}</div>

    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">👤</span>
          </div>
          <input
            v-model="username"
            id="username"
            type="text"
            class="form-control"
            placeholder="Username"
            required
          >
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input
            v-model="password"
            id="password"
            type="password"
            class="form-control"
            placeholder="Password"
            required
          >
        </div>
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-primary">Log in</button>
      </div>
    </form>
  </div>
</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    name: 'LoginForm',
    data () {
      return {
        username: '',
        password: '',
        error: null
      }
    },
    methods: {
      onSubmit () {
        this.error = null
        this.$store.dispatch('auth/login', {username: this.username, password: this.password}).then(() => {
          this.$router.push('/')
        }).catch(() => {
          this.error = 'Could not login with the provided credentials.'
        })
      }
    }
  })
</script>

<style scoped>
#container {
  width: 30em;
}
</style>
