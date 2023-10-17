<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      show: true
    }
  },
  methods: {
    async onFormSubmit(event) {
        const formData = new FormData();
        formData.append('username', this.form.username);
        formData.append('password', this.form.password);

        try{
            await this.$auth.loginWith('local', {data: formData, headers: {'Content-Type': 'application/x-www-form-urlencoded'}});
            this.$router.push("/authors")
        }catch(error) {
            this.$toast.error("Unable to login!")
        }
    }
  }
}
</script>

<template>
  <b-container>
    <div>
      <b-form @submit.prevent="onFormSubmit" v-if="show" class="mt-5">
        <h1>Login</h1>
        <b-form-group
          id="input-group-1"
          label="Username:"
          label-for="input-username"
        >
          <b-form-input
            id="input-username"
            v-model="form.username"
            type="text"
            placeholder="Enter Username"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-password"
          label="Username:"
          label-for="input-2"
        >
          <b-form-input
            id="input-password"
            v-model="form.password"
            type="password"
            placeholder="Enter Password"
            required
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Login</b-button>
      </b-form>
    </div>
  </b-container>
  </template>
