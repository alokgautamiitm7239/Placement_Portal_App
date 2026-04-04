<script>
import axios from 'axios'
export default{
    data(){
        return{
            token: localStorage.getItem("token"),
            formData:{
            job_title:"",
            branch:"",
            cgpa:"",
            year:"",
            deadline:"",
            },
            err:""
        }
    },
    methods:{
        createDrive(){
            const response=axios.post("http://127.0.0.1:5000/api/company/create_drive", this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token

                    }   
            })
            response
            .then(res=>{
                  this.$router.push("/company/dashboard")
           })
            .catch(err => {
              this.err=err.response.data.message
            })

           
        }
    }
}
</script>

<template>
    <form @submit.prevent="createDrive()">
        <div class=" container d-flex justify-content-center align-items-center vh-100">
        
        <div class="card p-4 shadow" style="width: 350px;">
            
            <h3 class="text-center mb-3">Create Drive</h3>

            <div class="mb-2 ">
            <label for="exampleInputEmail1" class="form-label" >Job Title</label>
            <input type="text" class="form-control" id="exampleInputEmail1" v-model="formData.job_title" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label" >Eligible branch</label>
            <input type="text" class="form-control" id="exampleInputPassword1" v-model="formData.branch" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label">Minimum CGPA</label>
            <input type="text" class="form-control"  v-model="formData.cgpa" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label">Eligible Year</label>
            <input type="text" class="form-control"  v-model="formData.year" required>
            </div>

            <div class="mb-2">
            <label for="exampleInputPassword1" class="form-label">Deadline</label>
            <input type="text" class="form-control"  v-model="formData.deadline" required>
            </div>

            <div class="mb-2 form-check">
            <label class="form-check-label" for="exampleCheck1">Remember me</label>
            </div>

            <button type="submit" class="btn btn-primary w-100">Done </button>
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