<script>

</script>

<template>
 <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
  <div class="container-fluid">

    <a class="navbar-brand fw-bold" href="#">Placement Portal</a>


      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link active" href="/">Home</a>
        </li>
      </ul>

      <div class="d-flex">
        <button class="btn btn-outline-light rounded-pill px-4 me-2" @click="this.$router.push('/login')">
          Login
        </button>
        <button class="btn btn-primary rounded-pill px-4 shadow-sm" @click="this.$router.push('/register')">
          Register
        </button>
      </div>

    </div>
</nav>
   
</template>