<script>
import { RouterLink } from 'vue-router';
import Register from './Register.vue';
import axios from 'axios';
export default{
  components: {Register},

   data(){
    return {
      token:"",
      userData:{
        "approved_drive":[]
      },
      search:"",
      applied:[],
      err:"",
    }
   },

   mounted(){
    this.loadToken()
    this.loadUser()
   },
   computed: {
    SearchDrives() {
         return this.userData.approved_drive.filter(drive => {

    const search =
      drive.company_name.toLowerCase().includes(this.search.toLowerCase()) ||
      drive.job_title.toLowerCase().includes(this.search.toLowerCase())  ||
      drive.branch.toLowerCase().includes(this.search.toLowerCase())||
      drive.location.toLowerCase().includes(this.search.toLowerCase())
    return search})
    },
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

    StudentApply: function(id){

        if (!this.applied.includes(id)) {
            this.applied.push(id)
            }

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
     },

    async startDownload() {
                
                try {
                    const res = await axios.get("http://127.0.0.1:5000/export_csv/1")
                    const taskId = res.data.id

                    setTimeout(() => {
                    const link = document.createElement("a")
                    link.href = `http://127.0.0.1:5000/api/csv_result/${taskId}`
                    document.body.appendChild(link)
                    link.click()
                    link.remove()

                    alert("CSV downloaded successfully!")

                    }, 2000) 

                } catch (error) {
                    console.error("Error:", error)
                }
            }
               
    }
}


   






</script>

<template>

    <div v-if="userData.message !== 'Register student first'">
            <div class="d-flex align-items-center justify-content-between p-3 bg-light rounded shadow-sm">
                    <h5 class="mb-0">
                    Welcome : 
                    <span class="text-primary">{{ userData.name}}</span>
                    </h5>
            

            <RouterLink to="/student/history">
                    <p>Placement History → </p>
            </RouterLink> </div>

            <div class="container mt-4" >
                    <div>
                        <h5 class="fontstyle bg-success">Placement Drives</h5>
                        <div class="d-flex justify-content-between align-items-center m-3">

                            <input type="text" v-model="search" class="form-control w-50" 
                                placeholder="Search by company or job title or branch or location ..."/>


                            <div> <button class="btn btn-dark btn-sm" @click="startDownload">Download CSV</button></div>

                            </div>

                    <div  >
                        <table class="table m-4 " v-if="SearchDrives && SearchDrives.length > 0">
                            <thead>
                                <tr>
                                <th scope="col">Company</th>
                                <th scope="col">Job Title</th>
                                <th scope="col">Eligibility Criteria</th>
                                <th scope="col">Location</th>
                                <th scope="col">Salary</th>
                                <th scope="col">Deadline</th>
                            
                                </tr>
                            </thead>
                            <tbody v-for="drive in SearchDrives" key="drive.id">
                                <tr>
                                <td>{{ drive.company_name }}</td>
                                <td>{{ drive.job_title }}</td>
                                <td>
                                     <div>Qualification - {{ drive.qualification }}</div>
                                    <div>Branch - {{ drive.branch }}</div>
                                    <div>Minimum CGPA - {{ drive.cgpa }}</div>
                                    <div>Experience - {{ drive.experience_year }} Year</div>  
                                </td>
                                <td>{{ drive.location }}</td>
                                <td>{{ drive.salary }}</td>
                                <td>{{ drive.deadline }}</td>
                                <td>
                                <div class="container">
                                    <div class="row">
                                        <div v-if="!applied.includes(drive.id)" class="col-md-7">
                                            <button type="button" class="btn btn-success" @click="StudentApply(drive.id)" >Apply</button>
                                        </div>
                                        <div v-else class="col-md-7">
                                            <button type="button" class="btn btn-secondary" disabled>Applied</button>
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

    </div>

    
                        
    <div v-else>
        <Register @registered="loadUser()" />
    </div>
    
</template>