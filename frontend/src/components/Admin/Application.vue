<script>
import axios from 'axios';
export default{
   data(){
    return {
      token:"",
      userData:"",
      showPopup:false
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
       const response=axios("http://127.0.0.1:5000/api/admin/application",{
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

    }
}

   






</script>

<template>
    <div class="container mt-4" >
     <table class="table m-4 " >
        <thead>
            <tr>
            <th scope="col">Student ID</th>
            <th scope="col">Name</th>
            <th scope="col">Company</th>
            <th scope="col">Job Title</th>
            <th scope="col">Date</th>
            <th scope="col">Action</th>
           
            </tr>
        </thead>
        <tbody v-for="application in userData.applications" key="application.id">
            <tr>
            <th scope="row" >{{ application.student_id }}</th>
            <td>{{ application.student_name }}</td>
            <td>{{ application.company_name }}</td>
            <td>{{ application.job_title}}</td>
            <td>{{ application.date }}</td>
            <td>
              <div class="container">
                  <div class="col-md-6">
                    <button type="button" class="btn btn-success w-100" @click="this.showPopup = true" >View</button>
                  </div>
                </div>
            </td>
            </tr>
        </tbody>
        </table>
    </div>

    <div v-if="this.showPopup" v-for="application in userData.applications" key="application.id" class="popup mt-4">
      <div class="popup-content">
        <h2>Application Details</h2>
        <p>Name: {{ application.student_name }}</p>
        <p>Branch: {{ application.branch }}</p>
        <p>CGPA: {{ application.cgpa }}</p>
        <p>Experience: {{ application.experience_year }} years</p>
        <p>Skills: {{ application.skills }}</p>
        <button class="btn btn-danger" @click="showPopup = false">Close</button>
      </div>
    </div>

    
</template>




<style>
.popup {
  position:fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
}

.popup-content {
  background: white;
  padding: 20px;
  width: 300px;
  margin: 100px auto;
  border-radius: 8px;
}
</style>