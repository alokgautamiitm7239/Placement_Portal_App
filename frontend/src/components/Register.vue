<script>
import axios from 'axios'
export default{
    data(){
        return{
            formData:{
            email:"",
            password:"",
            username:"",
            role:"",
            token:"",
            },
            err:""
        }
    },
    methods:{
        userRegister(){
            const response=axios.post("http://127.0.0.1:5000/api/register", this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    }   
            })
            response
            .then(res=>{
                  this.$router.push("/login")
           })
            .catch(err => {
              this.err=err.response.data.message
            })

           
        }
    }
}
</script>

<template>
    <form @submit.prevent="userRegister">
        <div class=" container d-flex justify-content-center align-items-center vh-100">
        
        <div class="card p-4 shadow" style="width: 350px;">
            
            <h3 class="text-center mb-3">Register</h3>

            <div class="mb-2 ">
            <label for="exampleInputEmail1" class="form-label" >Email</label>
            <input type="email" class="form-control" id="exampleInputEmail1" v-model="formData.email" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label" >Password</label>
            <input type="password" class="form-control" id="exampleInputPassword1" v-model="formData.password" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label">Username</label>
            <input type="text" class="form-control"  v-model="formData.username" required>
            </div>

            <div class="mb-3">
            <label for="role" class="form-label">Select Role</label>
            <select 
                class="form-select" id="role" v-model="formData.role" required>
                <option disabled value="">-- Select Role --</option>
                <option value="student">student</option>
                <option value="company">company</option>
            </select>
            </div>

            <div class="mb-2 form-check">
            <label class="form-check-label" for="exampleCheck1">Remember me</label>
            </div>

            <button type="submit" class="btn btn-primary w-100">Register</button>
            <p class="err" v-if="err">{{ this.err }}</p>

        </div>

        </div>
    </form>
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

</style>required