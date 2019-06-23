import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      props: (route) => ({ text: route.query.text }),
      component: Home
    },
    { 
      path: '*', 
      redirect: '/' 
    }
  ]
})
