import {createWebHistory,createRouter} from "vue-router";
import HomePage from "./components/HomePage.vue"
import LoginPage from "./components/LoginPage.vue";
import Student from "./components/Admin/Student.vue";
import Company from "./components/Admin/Company.vue";
import Drive from "./components/Admin/Drive.vue";
import Application from "./components/Admin/Application.vue";
import Dashboard from "./components/Admin/Dashboard.vue";

const routes=[
    {path:"/",component:HomePage},
    {path:"/login",component:LoginPage},
    {path: "/admin",
    children: [
      { path: "dashboard", component:Dashboard},
      { path: "student", component: Student },
      { path: "company", component: Company },
      { path: "drive", component: Drive },
      { path: "application", component: Application },
    ],
  },

]

export const router=createRouter({
    history:createWebHistory(),
    routes
})
