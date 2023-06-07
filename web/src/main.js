import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import '@/assets/css/reset.css'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'

//引入fontawesome 图标库
import '@/assets/fontawesome/css/fontawesome.css'
import '@/assets/fontawesome/css/all.css'

Vue.prototype.$axios = axios

Vue.config.productionTip = false

Vue.use(ElementUI);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
