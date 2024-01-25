import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import DashboardView from "../views/DashboardView.vue"
import NewpostView from "../views/NewpostView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path : '/new',
      name : 'new',
      component : NewpostView
    }
  ]
})

export default router
