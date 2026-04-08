<script>
import axios from 'axios';
export default{
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
    }
}
</script>

<template>
            <div class="container mt-4" >
                    <div>
                        <h5 class="fontstyle bg-success">Application History</h5>
                        <table class="table m-4 " >
                            <thead>
                                <tr>
                                <th scope="col">Company</th>
                                <th scope="col">Job Title</th>
                                <th scope="col">Application Status</th>
                            
                                </tr>
                            </thead>
                            <tbody v-for="drive in userData.applied_drive" key="drive.id">
                                <tr>
                                <td>{{ drive.company_name }}</td>
                                <td>{{ drive.job_title }}</td>
                                <td>{{ drive.status}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
            </div>
</template>