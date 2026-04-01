<script>
import axios from 'axios'
export default{
    data(){
        return{
            formData:{
            email:"",
            password:"",
            token:"",
            },
            err:""
        }
    },
    methods:{
        userLogin(){
            const response=axios.post("http://127.0.0.1:5000/api/login", this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    }
            })
            response
            .then(res=>{
              if(res.status==200){
                this.token=res.data["auth-token"]
                localStorage.setItem("token",res.data["auth-token"])
                if(res.data.role=="admin"){
                  this.$router.push("/admin/dashboard")
                }else if(res.data.role=="student"){
                  this.$router.push("/student/dashboard")
                }else{
                  this.$router.push("/company/dashboard")
                }
              }
           })
            .catch(err => {
              this.err=err.response.data.message
            })

           
        }
    }
}
</script>

<template>
    <div class=" container d-flex justify-content-center align-items-center vh-100">
  
  <div class="card p-4 shadow" style="width: 350px;">
    
    <h3 class="text-center mb-3">Login</h3>

    <div class="mb-2 ">
      <label for="exampleInputEmail1" class="form-label">Email</label>
      <input type="email" class="form-control" id="exampleInputEmail1" v-model="formData.email">
    </div>

    <div class="mb-3">
      <label for="exampleInputPassword1" class="form-label">Password</label>
      <input type="password" class="form-control" id="exampleInputPassword1" v-model="formData.password">
    </div>

    <div class="mb-3 form-check">
      <label class="form-check-label" for="exampleCheck1">Remember me</label>
    </div>

    <button type="submit" class="btn btn-primary w-100" @click="userLogin">Login</button>
    <p class="err" v-if="err">{{ this.err }}</p>

  </div>

</div>
    
</template>

<style>
.err{
  color: red;
  margin-top:15px;
  display: flex;
  justify-content: center;
  font-family: cursive;
  font-size: 12px;
}

</style>
