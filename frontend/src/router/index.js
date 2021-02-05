import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Doctor from '../views/Doctor.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    props: (route) => ({ currentPage: route.query.page || 1 }),
    meta: {
      title: 'Meta. Список психотерапевтов'
    }
  },
  {
    path: '/doctor/:id',
    name: 'Doctor',
    component: Doctor,
    props: true,
    meta: {
      title: 'Meta. Страница психотерапевта'
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})

export default router
