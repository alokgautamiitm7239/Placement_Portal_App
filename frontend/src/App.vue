<script >
import Navigation from './components/Navigation.vue';
import Footer from './components/Footer.vue';
export default {
  name: "App",
  components: {
    Navigation,
    Footer
  },
  data() {
    return {
      loggedIn: !!localStorage.getItem("token")
    }
  },
  methods: {
    loginHandle() {
      this.loggedIn = true
    },
    logoutHandle() {
      this.loggedIn = false
    }
  }
}

</script>

<template>
<Navigation :loggedIn="loggedIn" @logout="logoutHandle"/>
  
  <RouterView v-if="$route.path === '/login'" :loggedIn="loggedIn" @login="loginHandle" ></RouterView>
  <RouterView v-else > </RouterView>
 <Footer></Footer>
</template>
