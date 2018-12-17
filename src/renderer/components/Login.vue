<template>
  <div class="container" id="container">
    <p class="text-muted">
      <router-link to="home">Home</router-link>
    </p>
    <h1>Sign in</h1>
    <p class="text-muted">Enter your Polyphona account details to sign in.</p>

    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">👤</span>
          </div>
          <input id="username" type="text" class="form-control" placeholder="Username" required/>
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input id="password" type="password" class="form-control" placeholder="Password" required/>
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
    methods: {
      onSubmit () {
        alert('TODO')
      }
    }
  })
</script>

<style scoped>
  #container {
    width: 30em;
    margin-top: 3em;
  }

</style>