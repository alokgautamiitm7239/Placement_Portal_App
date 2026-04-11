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
            experience_year:"",
            deadline:"",
            qualification:"",
            salary:"",
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
                  alert("Drive created successfully wait for approval")
           })
            .catch(err => {
              this.err=err.response.data.message
            })

           
        }
    }
}
</script>

<template>
 <div >
    <form @submit.prevent="createDrive()">
        <div class=" container d-flex justify-content-center align-items-center">
        
        <div class="card p-4 shadow mt-4" style="width: 500px;">
            
            <h3 class="text-center mb-2">Create Drive</h3>

            <div class="mb-1 ">
            <label for="job_title" class="form-label" >Job Title</label>
            <input type="text" class="form-control" id="job_title" v-model="formData.job_title" required>
            </div>

            <div class="mb-1">
            <label  class="form-label" >Required Qualification</label>
            <input type="text" class="form-control"  v-model="formData.qualification" required>
            </div>

            <div class="mb-1">
            <label  class="form-label" >Eligible branch</label>
            <input type="text" class="form-control"  v-model="formData.branch" required>
            </div>

            <div class="mb-1">
            <label  class="form-label">Minimum CGPA</label>
            <input type="number" class="form-control"  v-model="formData.cgpa" required>
            </div>

            <div class="mb-1">
            <label  class="form-label">Experience(in Year)</label>
            <input type="number" class="form-control"  v-model="formData.experience_year" required>
            </div>

            <div class="mb-1">
            <label  class="form-label">Salary</label>
            <input type="text" class="form-control"  v-model="formData.salary" required>
            </div>

            <div class="mb-1">
            <label  class="form-label">Deadline</label>
            <input type="date" class="form-control"  v-model="formData.deadline" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Done </button>
            <p class="err" v-if="err">{{ this.err }}</p>

        </div>

        </div>
    </form>
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

</style>required