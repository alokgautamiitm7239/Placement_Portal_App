<script>
import axios from 'axios';
export default{
   data(){
    return {
      token:"",
      userData:""
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
       const response=axios("http://127.0.0.1:5000/api/admin/drive",{
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

    updateStatus:function(id,status){
       const response= axios.put(`http://127.0.0.1:5000/api/admin/drive/${id}`,{ status: status },{
            headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":this.token
                    }
            });
            response
            .then(res=>  this.loadUser())
            .catch (err=> {
               console.log(err.response);
            } )
      },


    }
}

   






</script>

<template>
    <div class="container mt-4" >
            <h5 class="fontstyle bg-success">Approved Drive</h5>
            <table class="table m-4 " v-if="userData.approved_drive && userData.approved_drive.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Drive ID</th>
                    <th scope="col">Company Name</th>
                    <th scope="col">Job Title</th>
                    <th scope="col">Deadline</th>
                    <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody v-for="drive in userData.approved_drive" key="drive.id">
                    <tr>
                    <th scope="row" >{{ drive.id }}</th>
                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="container fontstyle mt-4">
                <p>No approved company ✅ </p>
            </div>
    </div>>

    <div class="container mt-4">
           <h5 class="fontstyle bg-warning">Pending Drive</h5>

            <table class="table m-4 " v-if="userData.pending_drive && userData.pending_drive.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Drive ID</th>
                    <th scope="col">Company Name</th>
                    <th scope="col">Job Title</th>
                    <th scope="col">Deadline</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody v-for="drive in userData.pending_drive" key="drive.id">
                    <tr>
                    <th scope="row" >{{ drive.id }}</th>

                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>
                    <td>
                    <div class="container">
                        <div class="row">
                        <div class="col-md-4" >
                            <button type="button" class="btn btn-success w-100"  @click="updateStatus(drive.id,status='approved')">Approve</button>
                        </div>
                        <div class="col-md-4">
                            <button type="button" class="btn btn-danger w-100" @click="updateStatus(drive.id , status='rejected')" >Reject</button>
                        </div>
                        </div>
                    </div>
                    </td>
                    </tr>
                </tbody>
            </table >

            <div v-else class="container fontstyle mt-4">
                <p>No pending company ⚠️</p>
            </div>

    </div>

    <div class="container mt-4">
           <h5 class="fontstyle bg-danger">Rejected Drive</h5>

            <table class="table m-4 " v-if="userData.rejected_drive && userData.rejected_drive.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Drive ID</th>
                    <th scope="col">Company Name</th>
                    <th scope="col">Job Title</th>
                    <th scope="col">Deadline</th>
                    <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody v-for="company in userData.rejected_drive" key="drive.id">
                    <tr>
                    <th scope="row" >{{ drive.id }}</th>
                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>
                    </tr>
                </tbody>
            </table >

            <div v-else class="container fontstyle mt-4">
                <p> No rejected company ❌</p>
            </div>

    </div>
    
</template>

<style>
.fontstyle{
    display: flex;
    justify-content: center;
    font-family: serif;
    font-weight: bold;
    }
</style>