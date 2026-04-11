import {createWebHistory,createRouter} from "vue-router";
import HomePage from "./components/HomePage.vue"
import LoginPage from "./components/LoginPage.vue";
import Register from "./components/Register.vue";
import Student from "./components/Admin/Student.vue";
import Company from "./components/Admin/Company.vue";
import Drive from "./components/Admin/Drive.vue";
import Application from "./components/Admin/Application.vue";
import Dashboard from "./components/Admin/Dashboard.vue";
import Company_Dashboard from "./components/Company/Dashboard.vue";
import Drive_register from "./components/Company/Drive_register.vue";
import Drive_application from "./components/Company/Drive_application.vue";
import Student_Dashboard from "./components/Student/Dashboard.vue";
import StudentApplication from "./components/Student/Application.vue";
import ApplicationHistory from "./components/Student/ApplicationHistory.vue";
import Edit from "./components/Student/Edit.vue";


const routes=[
    {path:"/",component:HomePage},
    {path:"/login",component:LoginPage},
    {path:"/register",component:Register},

    {path: "/admin",
    children: [
      { path: "dashboard", component:Dashboard},
      { path: "student", component: Student },
      { path: "company", component: Company },
      { path: "drive", component: Drive },
      { path: "application", component: Application },
    ],
  },

    {path: "/company",
    children: [
      { path: "dashboard", component:Company_Dashboard},
      { path: "create_drive", component:Drive_register},
      { path: "application", component:Drive_application },
  
    ],
  },


    {path: "/student",
    children: [
      { path: "dashboard", component:Student_Dashboard},
      { path: "application", component:StudentApplication},
      { path: "history", component:ApplicationHistory},
      { path: "editprofile", component: Edit },
    ],
  },

]

export const router=createRouter({
    history:createWebHistory(),
    routes
})
