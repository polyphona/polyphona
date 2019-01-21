<template>
  <div class="container" id="container">
    <p class="text-muted">
      <router-link to="home">Home</router-link>
    </p>
    <h1>Create an account</h1>
    <p class="text-muted">Enter your account details.</p>

    <div class="alert alert-danger" role="alert" v-if="error">
      {{ error }}
    </div>

    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">👤</span>
          </div>
          <input v-model="username" id="username" type="text" class="form-control" placeholder="Enter username…"
                 required/>
        </div>
      </div>

      <div class="form-group">
        <label for="first-name">First name</label>
        <div class="input-group">
          <input v-model="firstName" id="first-name" type="text" class="form-control"
                 placeholder="Enter your first name…" required/>
        </div>
      </div>

      <div class="form-group">
        <label for="last-name">Last name</label>
        <div class="input-group">
          <input v-model="lastName" id="last-name" type="text" class="form-control" placeholder="Enter your last name…"
                 required/>
        </div>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input v-model="password" id="password" type="password" class="form-control" placeholder="Enter password…"
                 required/>
        </div>
      </div>

      <div class="form-group">
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">🔒</span>
          </div>
          <input v-model="passwordConfirm" id="password_conformity" type="password" class="form-control"
                 placeholder="Confirm password…" required/>
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
    data () {
      return {
        username: '',
        firstName: '',
        lastName: '',
        password: '',
        passwordConfirm: '',
        error: null
      }
    },
    methods: {
      onSubmit () {
        this.error = null
        if (this.password !== this.passwordConfirm) {
          this.error = 'Passwords do not match.'
          return
        }
        this.$store.dispatch('auth/register', {
          username: this.username,
          firstName: this.firstName,
          lastName: this.lastName,
          password: this.password
        }).then(() => {
          this.$router.push('/')
        }).catch((e) => {
          console.error(e)
          this.error = 'An error occurred while trying to create your account.'
        })
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
