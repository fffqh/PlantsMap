//引入Vue核心库
import Vue from 'vue'
//引入Vuex
import Vuex from 'vuex'
//应用Vuex插件
Vue.use(Vuex)

//准备actions对象——响应组件中用户的动作
const actions = {

}
//准备mutations对象——修改state中的数据
const mutations = {
  SETUSER(state, user) {
    console.log('SETUSER被调用!')
    state.user = user
  },
  SETLOGIN(state, login) {
    console.log('SETLOGIN被调用！')
    state.login = Boolean(login)
  }
}
//准备state对象——保存具体的数据
const state = {
  user:{
    name:'',
    id:-1,
  },
  login:false,
  // host:"http://47.111.2.163:5000"
  host:"http://localhost:5000/api-fqh"
  // host:'http://124.71.169.200:5001/api-fqh'
}

//创建并暴露store
export default new Vuex.Store({
  actions,
  mutations,
  state
})
