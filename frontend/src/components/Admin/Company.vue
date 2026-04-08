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
       const response=axios("http://127.0.0.1:5000/api/admin/company",{
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


    blockUser:function(id,status){
       const response= axios.put(`http://127.0.0.1:5000/api/admin/Bcompany/${id}`,{ active: status },{
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

    updateStatus:function(id,status){
       const response= axios.put(`http://127.0.0.1:5000/api/admin/company/${id}`,{ status: status },{
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
    <div class="container-fluid mt-4" >
            <h5 class="fontstyle bg-success">Approved Company</h5>
            <table class="table m-4 " v-if="userData.approved_company && userData.approved_company.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Company ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Website</th>
                    <th scope="col">Contact info</th>
                    <th scope="col">Location</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                
                    </tr>
                </thead>
                <tbody v-for="company in userData.approved_company" key="company.id">
                    <tr>
                    <th scope="row" >{{ company.id }}</th>
                    <td>{{ company.company_name }}</td>
                    <td>{{ company.website }}</td>
                    <td>{{ company.contact }}</td>
                    <td>{{ company.location }}</td>
                    <td>{{ company.status }}</td>
                    <td>
                    <div class="container">
                        <div class="row">
                        <div class="col-md-7" v-if="!company.active">
                            <button type="button" class="btn btn-success w-100"  @click="blockUser(company.id,status=true)">Unblock</button>
                        </div>
                        <div class="col-md-7" v-else>
                            <button type="button" class="btn btn-danger w-100" @click="blockUser(company.id , status=false)" >Block</button>
                        </div>
                        </div>
                    </div>
                    </td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="container fontstyle mt-4">
                <p>No company </p>
            </div>
    </div>

    <div class="container-fluid mt-4">
           <h5 class="fontstyle bg-warning">Pending Company</h5>

            <table class="table m-4 " v-if="userData.pending_company && userData.pending_company.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Company ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Website</th>
                    <th scope="col">Contact info</th>
                    <th scope="col">Location</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody v-for="company in userData.pending_company" key="company.id">
                    <tr>
                    <th scope="row" >{{ company.id }}</th>

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.website }}</td>
                    <td>{{ company.contact }}</td>
                    <td>{{ company.location }}</td>
                    <td>{{ company.status }}</td>
                    <td>
                    <div class="container">
                        <div class="row">
                        <div class="col-md-4" >
                            <button type="button" class="btn btn-success w-100"  @click="updateStatus(company.id,status='approved')">Approve</button>
                        </div>
                        <div class="col-md-4">
                            <button type="button" class="btn btn-danger w-100" @click="updateStatus(company.id , status='rejected')" >Reject</button>
                        </div>
                        </div>
                    </div>
                    </td>
                    </tr>
                </tbody>
            </table >

            <div v-else class="container fontstyle mt-4">
                <p>No company</p>
            </div>

    </div>

    <div class="container-fluid mt-4">
           <h5 class="fontstyle bg-danger">Rejected Company</h5>

            <table class="table m-4 " v-if="userData.rejected_company && userData.rejected_company.length > 0">
                <thead>
                    <tr>
                    <th scope="col">Company ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Website</th>
                    <th scope="col">Contact info</th>
                    <th scope="col">Location</th>
                    <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody v-for="company in userData.rejected_company" key="company.id">
                    <tr>
                    <th scope="row" >{{ company.id }}</th>
                    <td>{{ company.company_name }}</td>
                    <td>{{ company.website }}</td>
                    <td>{{ company.contact }}</td>
                    <td>{{ company.location }}</td>
                    <td>{{ company.status }}</td>
                    </tr>
                </tbody>
            </table >

            <div v-else class="container fontstyle mt-4">
                <p> No company</p>
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