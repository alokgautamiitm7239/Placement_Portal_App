<script>
import axios from 'axios';
export default{
   data(){
    return {
      token:"",
      userData:""
    }
   },
   mounted(){
    this.loadToken()
    this.loadUser()
   },
   methods:{
    loadToken: function(){
      const token=localStorage.getItem("token")
      this.token=token
    },
    loadUser:function(){
       const response=axios("http://127.0.0.1:5000/api/admin/dashboard",{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    }
            })
            response
            .then(res=>{
              this.userData=res.data
              console.log(res.data)
            })
            .catch(err => {
              console.log(err.response.data)
            })

           
        }
    }
   
}
</script>

<template>
  <div class="row g-4 mb-4 mt-4" id="container" v-if="token">

    <div class="d-flex align-items-center justify-content-between p-3 ">
        <h4 class="mx-4">
          Welcome : 
          <span class="text-primary">{{ userData.username}}</span>
        </h4>
  </div>

    <div class="col-md-3">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <h2>{{ this.userData.student }}</h2>
        <p class="text-muted">Total Students</p>
        <RouterLink to="/admin/student" class="text-primary"> Manage Students →</RouterLink>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <h2>{{ this.userData.company }}</h2>
        <p class="text-muted">Registered Companies</p>
        <RouterLink to="/admin/company" class="text-primary"> Manage Companies →</RouterLink>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <h2>{{ this.userData.drive }}</h2>
        <p class="text-muted">Total Placement Drives</p>
        <RouterLink to="/admin/drive" class="text-danger"> Manage Drives →</RouterLink>
      </div>
    </div>

    <div class="col-md-3">
      <div class="card p-4 shadow-sm border-0 rounded-4 ">
        <h2>{{ this.userData.application }}</h2>
        <p class="text-muted">Total Applications</p>
        <RouterLink to="/admin/application" class="text-warning"> Manage Applications →</RouterLink>
      </div>
    </div>

  </div>
</template>

<style>
</style>