import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import './sw'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueI18n from 'vue-i18n'
import locale from './utils/locale'

Vue.use(VueI18n)

Vue.config.productionTip = false

const i18n = new VueI18n({
  locale: navigator.language, // set locale
  messages: locale
})


new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
