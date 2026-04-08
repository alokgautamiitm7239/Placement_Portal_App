<script>
import axios from 'axios';
export default{
    data(){
        return{
            token:"",
            formData: {
                date: "",
                resume: "",
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

        StudentRegister(){
            const d_id=this.$route.query.drive_id
            const s_id=this.$route.query.student_id
            const response=axios.post(`http://127.0.0.1:5000/api/student/application/${d_id}/${s_id}`, this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    },                    
            })
            response
            .then(res=>{
                 this.$emit("registered")}
            )
            .catch(err => {
              this.err=err.response
            })
        }

    }
}
</script>

<template>
            <form @submit.prevent="StudentRegister()">
               <div class=" mt-2 container d-flex justify-content-center align-items-center vh-100">
                
                <div class="card p-4 shadow" style="width: 500px;">
                    
                    <h3 class="text-center mb-2">Upload resume </h3>

                    <div class="mb-1 ">
                    <label for="exampleInputEmail1" class="form-label" >Name </label>
                    <input type="text" class="form-control" id="exampleInputEmail1" v-model="formData.name" required>
                    </div>

                    <div class="mb-1">
                    <label for="exampleInputPassword1" class="form-label" >Skills</label>
                    <input type="text" class="form-control" id="exampleInputPassword1" v-model="formData.skills" required>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">Register</button>
                    <p class="err" v-if="err">{{ this.err }}</p>

                </div>
                </div>
            </form>
</template>