<script>
import { RouterLink } from 'vue-router';
import Register from './Register.vue';
import axios from 'axios';
export default{
  components: {Register},

   data(){
    return {
      token:"",
      userData:"",
      err:""
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
       const response=axios("http://127.0.0.1:5000/api/student/dashboard",{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    }
            })
            
            response
            .then(res=>{
              this.userData=res.data
              console.log(res)
            })
            .catch(err => {
              console.log(err.response.data)
            })
        },

    StudentApply(id){
        const response=axios(`http://127.0.0.1:5000/api/student/application/${id}/${this.userData.id}`,{
            headers:{
                "Content-Type":"application/json",
                "Authentication-Token":this.token
                },                    
        })
        response
        .then(res=>{this.loadUser()}
        )
        .catch(err => {
            this.err=err.response
        })
    }



    }
}

   






</script>

<template>

    <div v-if="userData.message !== 'Register student first'">
            <div class="d-flex align-items-center justify-content-between p-3 bg-light rounded shadow-sm">
                    <h3 class="mb-0">
                    Welcome : 
                    <span class="text-primary">{{ userData.name}}</span>
                    </h3>
            </div>

            <RouterLink to="/student/history">
                    <button class=" btn btn-primary ">History</button>
            </RouterLink>

            <div class="container mt-4" >
                    <div>
                        <h5 class="fontstyle bg-success">Placement Drives</h5>
                        <table class="table m-4 " v-if="userData.approved_drive && userData.approved_drive.length > 0">
                            <thead>
                                <tr>
                                <th scope="col">Company</th>
                                <th scope="col">Job Title</th>
                                <th scope="col">Eligibility Criteria</th>
                                <th scope="col">Deadline</th>
                            
                                </tr>
                            </thead>
                            <tbody v-for="drive in userData.approved_drive" key="drive.id">
                                <tr>
                                <td>{{ drive.company_name }}</td>
                                <td>{{ drive.job_title }}</td>
                                <td>
                                   <tr>Qualification - {{ drive.qualification }}</tr>
                                   <tr>Branch - {{ drive.branch }}</tr>
                                   <tr>Minimun CGPA - {{ drive.cgpa }}</tr>
                                   <tr>Experience - {{ drive.experience_year }} Year</tr>  
                                </td>
                                <td>{{ drive.deadline }}</td>
                                <td>
                                <div class="container">
                                    <div class="row">
                                    <div class="col-md-7">
                                        <button type="button" class="btn btn-secondary" @click="StudentApply(drive.id)" >Apply</button>
                                    </div>
                                    </div>
                                </div>
                                </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
            </div>

    </div>

    
                        
    <div v-else>
        <Register @registered="loadUser()" />
    </div>
    
</template>