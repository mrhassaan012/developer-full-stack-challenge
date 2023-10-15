<template>
    <div>
        <b-navbar toggleable="lg" type="light" variant="light">
            <b-container>
                <b-navbar-brand href="#">Full Stack Challenge</b-navbar-brand>

                <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav v-if="loggedIn">
                                    <nuxt-link to="/authors" class="nav-link">Authors</nuxt-link>
                    <nuxt-link to="/books" class="nav-link">Books</nuxt-link>
                </b-navbar-nav>

                <b-navbar-nav class="ml-auto">


                    <b-nav-item-dropdown v-if="loggedIn" right>
                    <template #button-content>
                        <em>{{ user.username }}</em>
                    </template>
                    <b-dropdown-item @click="userLogout()">Sign Out</b-dropdown-item>
                    </b-nav-item-dropdown>

                </b-navbar-nav>
                </b-collapse>
            </b-container>
        </b-navbar>

  </div>

</template>

<script>
export default {
  data() {
    return {
      loggedIn: false,
      user: {}
    };
  },
  methods: {
    async userLogout() {
      await this.$auth.logout();
      this.updateUserStatus()
      this.$router.push("/login")
    },
    updateUserStatus() {
      this.loggedIn = this.$auth.loggedIn;
      this.user = this.$auth.user;
    }
  },
  async asyncData({ $auth }) {
    return {
      loggedIn: $auth.loggedIn,
      user: $auth.user
    };
  },
  async mounted() {
    this.updateUserStatus();

    this.$watch(() => this.$auth.loggedIn, (newVal) => {
      this.loggedIn = newVal;
    });

    this.$watch(() => this.$auth.user, (newVal) => {
      this.user = newVal;
    });
  }
};
</script>