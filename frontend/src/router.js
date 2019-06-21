import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      props: (route) => ({ url: route.query.url, text: route.query.text, title: route.query.title }),
      component: Home
    }
  ]
})
