<script>
import axios from 'axios';
export default{
    data(){
        return{
            token:"",
            formData: {
                name: "",
                skills: "",
                course: "",
                branch: "",
                cgpa: "",
                experience_year: ""
                },
            err:""
        }
    },
    mounted(){
        this.loadToken()
    },
    methods:{
        loadToken: function(){
        const token=localStorage.getItem("token")
        this.token=token
        },

        editProfile(){
            const response=axios.put("http://127.0.0.1:5000/api/student/update_profile", this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    },                    
            })
            response
            .then(res=>{
                 this.$router.push("/student/dashboard")
                alert("Profile Updated Successfully")}
            )
            .catch(err => {
              this.err=err.response
            })
        }

    }
}
</script>

<template>
            <form @submit.prevent="editProfile()">
               <div class=" mt-2 container d-flex justify-content-center align-items-center vh-100">
                
                <div class="card p-4 shadow" style="width: 500px;">
                    
                    <h3 class="text-center mb-2">Update Profile</h3>

                    <div class="mb-1 ">
                    <label  class="form-label" >Name </label>
                    <input type="text" class="form-control"  v-model="formData.name" required>
                    </div>

                    <div class="mb-1">
                    <label  class="form-label" >Skills</label>
                    <input type="text" class="form-control"  v-model="formData.skills" required>
                    </div>

                    <div class="mb-1">
                    <label  class="form-label" >Qualification</label>
                    <input type="text" class="form-control"  v-model="formData.course" required>
                    </div>

                    <div class="mb-1">
                    <label  class="form-label">Branch</label>
                    <input type="text" class="form-control"  v-model="formData.branch" required>
                    </div>

                    <div class="mb-1">
                    <label  class="form-label">CGPA</label>
                    <input type="number"  class="form-control"  v-model="formData.cgpa" required>
                    </div>

                    <div class="mb-3">
                    <label  class="form-label">Experience (in year)</label>
                    <input type="number" class="form-control"  v-model="formData.experience_year" required>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">Update</button>
                    <p class="err" v-if="err">{{ this.err }}</p>

                </div>
                </div>
            </form>
</template>