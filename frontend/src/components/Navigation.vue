<script>
export default {
  props:["loggedIn"],
  emits:["logout"],

  computed:{
   islogged(){
    return this.loggedIn
   }
  },
  methods:{

    logout(){
      localStorage.clear()
      this.$emit("logout")
      this.$router.push("/")
    }
  }
}

</script>

<template>
 <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
  <div class="container-fluid">

    <a class="navbar-brand fw-bold" href="#">Placement Portal</a>


      <div class="d-flex align-items-center">
        <template v-if="!islogged">
          <button class="btn btn-outline-light rounded-pill px-4 me-2" @click="this.$router.push('/login')">
            Login
          </button>
          <button class="btn btn-primary rounded-pill px-4 shadow-sm" @click="this.$router.push('/register')">
            Register
          </button>
        </template>

        <template v-else>
          <button class="btn btn-danger rounded-pill px-4 shadow-sm" @click="logout()">
            Logout
          </button>
        </template>

      </div>

    </div>
</nav>
   
</template>