import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import '../theme/index.css'
import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router'
import store from './store'

// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap"
// 全局引入echarts
// import echarts from "echarts";
// Vue.prototype.$echarts = echarts;

//使用ElementUI
Vue.use(ElementUI);
//使用路由

Vue.use(VueRouter)
const RouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(to) {
  return RouterPush.call(this, to).catch(err => err)
}
const RouterReplace = VueRouter.prototype.replace
VueRouter.prototype.replace = function replace(to) {
  return RouterReplace.call(this, to).catch(err => err)
}

Vue.use(Vuex)
// 全局设置
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')
