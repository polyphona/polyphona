<template>
  <div class="container" id="container">
    <p class="text-muted">
      <router-link to="home">Home</router-link>
    </p>
    <h1>Create an account</h1>
    <p class="text-muted">Choose a username and password.</p>

    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">👤</span>
          </div>
          <input id="username" type="text" class="form-control" placeholder="Choose username" required/>
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input id="password" type="password" class="form-control" placeholder="Choose password" required/>
        </div>
      </div>

      <div class="form-group">
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input id="password_conformity" type="password" class="form-control" placeholder="Confirm password" required/>
        </div>
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-primary">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    name: 'RegisterForm',
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
