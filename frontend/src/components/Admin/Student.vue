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
       const response=axios("http://127.0.0.1:5000/api/admin/student",{
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
       const response= axios.put(`http://127.0.0.1:5000/api/admin/student/${id}`,{ active: status },{
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
      }
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
            <th scope="col">Branch</th>
            <th scope="col">CGPA</th>
            <th scope="col">Year</th>
            <th scope="col">Action</th>
           
            </tr>
        </thead>
        <tbody v-for="student in userData.students" key="student.id">
            <tr>
            <th scope="row" >{{ student.id }}</th>
            <td>{{ student.name }}</td>
            <td>{{ student.branch }}</td>
            <td>{{ student.cgpa }}</td>
            <td>{{ student.year }}</td>
            <td>
              <div class="container">
                <div class="row">
                  <div class="col-md-6" v-if="!student.active">
                    <button type="button" class="btn btn-success w-100"  @click="blockUser(student.id,status=true)">Unblock</button>
                  </div>
                  <div class="col-md-6" v-else>
                    <button type="button" class="btn btn-danger w-100" @click="blockUser(student.id , status=false)" >Block</button>
                  </div>
                </div>
              </div>
            </td>
            </tr>
        </tbody>
        </table>
    </div>
    
</template>