// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import router from './router'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'
import left from '@/components/left.vue'
import header from '@/components/header.vue'

import App from './App'

Vue.prototype.$ajax = axios
window.axios = axios
axios.defaults.withCredentials = true
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueResource)
// Vue.use($)
/* eslint-disable no-new */
// 创建组件构造器btn
var btn = Vue.extend({
  template: '<button>查看</button>'
})
// 注册组件，指定组件标签
Vue.component('search-btn', btn)
// 左侧导航栏
Vue.component('my-left', left)
// 顶部导航
Vue.component('my-header', header)
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App)
})