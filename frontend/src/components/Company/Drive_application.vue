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
       const id=this.$route.query.id
       const response=axios(`http://127.0.0.1:5000/api/company/drive/${id}`,{
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
       const response= axios.put(`http://127.0.0.1:5000/api/company/application/${id}`,{ status: status },{
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



<template >
    <div class="container mt-4" id="hello">
            <h5 class="fontstyle bg-success text-black">Shortlisted Applications</h5>
            <table class="table m-4 " v-if="userData.shortlisted_applications?.length">
                <thead>
                    <tr>
                    <th scope="col">Student name</th>
                    <th scope="col">Branch</th>
                    <th scope="col">CGPA</th>
                    <th scope="col">Skills</th>
                    <th scope="col">Status</th>
                
                    </tr>
                </thead>
                <tbody v-for="application in userData.shortlisted_applications" key="application.id">
                    <tr>
                    <th scope="row" >{{ application.student_name }}</th>
                    <td>{{ application.branch }}</td>
                    <td>{{ application.cgpa }}</td>
                    <td>{{ application.skills }}</td>
                    <td>{{ application.status }}✅</td>
                    </tr>
                </tbody>
            </table>

             <div v-else class="container fontstyle mt-4">
                <p> No Applications </p>
            </div>
    </div>

    <div class="container mt-4" >
            <h5 class="fontstyle bg-warning ">Applied Applications</h5>
            <table class="table m-4 " v-if="userData.applied_applications?.length">
                <thead>
                    <tr>
                    <th scope="col">Student name</th>
                    <th scope="col">Branch</th>
                    <th scope="col">CGPA</th>
                    <th scope="col">Skills</th>
                    <th scope="col">Action</th>
                
                    </tr>
                </thead>
                <tbody v-for="application in userData.applied_applications" key="application.id">
                    <tr>
                    <th scope="row" >{{ application.student_name }}</th>
                    <td>{{ application.branch }}</td>
                    <td>{{ application.cgpa }}</td>
                    <td>{{ application.skills }}</td>
                    <td>
                    <div class="container">
                        <div class="row">
                        <div class="col-md-3">
                            <button type="button" class="btn btn-success w-100"  @click="updateStatus(id=application.id , status='shortlisted')">Shortlist</button>
                        </div>
                        
                        <div class="col-md-3">
                            <button type="button" class="btn btn-danger w-100"  @click="updateStatus(id=application.id , status='rejected')">Reject</button>
                        </div>
                    </div>
                </div>
                    </td>
                    </tr>
                </tbody>
            </table>

             <div v-else class="container fontstyle mt-4">
                <p> No Applications </p>
            </div>
    </div>

    <div class="container mt-4" >
            <h5 class="fontstyle bg-danger">Rejected Applications</h5>
            <table class="table m-4 " v-if="userData.rejected_applications?.length">
                <thead>
                    <tr>
                    <th scope="col">Student name</th>
                    <th scope="col">Branch</th>
                    <th scope="col">CGPA</th>
                    <th scope="col">Skills</th>
                    <th scope="col">Status</th>
                
                    </tr>
                </thead>
                <tbody v-for="application in userData.rejected_applications" key="application.id">
                    <tr>
                    <th scope="row" >{{ application.student_name }}</th>
                    <td>{{ application.branch }}</td>
                    <td>{{ application.cgpa }}</td>
                    <td>{{ application.skills }}</td>
                    <td>❌{{ application.status }}</td>
                    </tr>
                </tbody>
            </table>

             <div v-else class="container fontstyle mt-4">
                <p> No Applications </p>
            </div>
    </div>
</template>