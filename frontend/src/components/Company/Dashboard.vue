<script>
import axios from 'axios';
export default{
   data(){
    return {
      token:"",
      userData:"",
      formData: {
        name: "",
        contact: "",
        website: "",
        location: "",
        },
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
       const response=axios("http://127.0.0.1:5000/api/company/dashboard",{
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
    companyRegister(){

            const response=axios.post("http://127.0.0.1:5000/api/company/register", this.formData,{
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    },                    
            })
            response
              .then(res => {
                this.loadUser()
            })
            .catch(err => {
              this.err=err.response.data.message
            })
        }

    }
}

   






</script>

<template>
   <div class="d-flex align-items-center justify-content-between p-3 bg-light rounded shadow-sm">
        <h3 class="mb-0">
          Company Name: 
          <span class="text-primary">{{ userData.name}}</span>
        </h3>
        <div >Status: {{ userData.status }}</div>

        <RouterLink to="/company/create_drive" v-if="userData.status =='approved'">
          <button class="btn btn-primary">
            + Create Drive
          </button>
        </RouterLink>
  </div>

    <div class="container mt-4" >
        <div v-if="userData.message !== 'Register the company first'">
            <h5 class="fontstyle bg-success">Drives</h5>
            <table class="table m-4 " v-if="userData.company_drive && userData.company_drive.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Drive ID</th>
                    <th scope="col">Job Title</th>
                    <th scope="col">Deadline</th>
                    <th scope="col">No of Applicant</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                
                    </tr>
                </thead>
                <tbody v-for="drive in userData.company_drive" key="company.id">
                    <tr>
                    <th scope="row" >{{ drive.id }}</th>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.application_len }}</td>
                    <td>{{ drive.status }}</td>
                    <td>
                    <div class="container">
                        <div class="row">
                        <div class="col-md-7">
                           <RouterLink :to="{path: '/company/application',query:{id:drive.id}}">
                            <button type="button" class="btn btn-success w-100"  >View</button>
                          </RouterLink>
                        </div>
                        </div>
                    </div>
                    </td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="container fontstyle mt-4">
                <p>No drive available </p>
                   <div class="col-md-2  mx-4" v-if="userData.status=='approved'" >
                    <RouterLink to="/company/create_drive">  
                      <button type="button" class="btn btn-primary w-100" >+ Create</button>
                    </RouterLink>
                           
                    </div>

            </div>
        </div>


        
        <div v-else>
            <form @submit.prevent="companyRegister()">
               <div class=" container d-flex justify-content-center align-items-center vh-100">
                
                <div class="card p-4 shadow" style="width: 350px;">
                    
                    <h3 class="text-center mb-3">Company Registration</h3>

                    <div class="mb-2 ">
                    <label for="exampleInputEmail1" class="form-label" >Name </label>
                    <input type="text" class="form-control" id="exampleInputEmail1" v-model="formData.name" required>
                    </div>

                    <div class="mb-2">
                    <label for="exampleInputPassword1" class="form-label" >Contact </label>
                    <input type="text" class="form-control" id="exampleInputPassword1" v-model="formData.contact" required>
                    </div>

                    <div class="mb-2">
                    <label for="exampleInputPassword1" class="form-label">Website</label>
                    <input type="text" class="form-control"  v-model="formData.website" required>
                    </div>

                    <div class="mb-2">
                    <label for="exampleInputPassword1" class="form-label">Location</label>
                    <input type="text" class="form-control"  v-model="formData.location" required>
                    </div>

                    <div class="mb-2 form-check">
                    <label class="form-check-label" for="exampleCheck1">Remember me</label>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">Register</button>
                    <p class="err" v-if="err">{{ this.err }}</p>

                </div>

                </div>
            </form>
        </div>
    </div>
    
</template>