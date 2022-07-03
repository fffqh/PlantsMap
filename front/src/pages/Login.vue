<template>
    <el-row>
      <el-col :span="9" :offset="7">
      <el-card class="box-card" :style="`background-color: ${cardColor};`">
        <!-- 表头 -->
        <div slot="header" class="clearfix">
          <span>{{stateName}}</span>
          <el-button @click.prevent="chgState" style="float: right; padding: 3px 0" type="text">{{toStateName}}</el-button>
        </div>
        <!-- 登录表单 -->
        <el-form label-position="left" ref="form" :model="form" label-width="100px">
          <el-form-item label="用户名">
            <el-input v-model="form.user_name" 
              suffix-icon="el-icon-user" 
              placeholder="请输入用户名">
            </el-input>
          </el-form-item>
          <el-form-item v-if="state" label="邮箱">
            <el-col :span="20">
              <el-input v-model="form.user_email"
                type="email"
                suffix-icon="el-icon-message" 
                placeholder="请输入邮箱地址">
              </el-input>
            </el-col>
            <el-col :span="3" :offset="1">
              <el-tooltip class="item" effect="dark" content="点击发送验证码至邮箱" placement="right">
              <el-button @click="getVerify" type="info" icon="el-icon-message" circle></el-button>
              </el-tooltip>
            </el-col>
          </el-form-item>
          <el-form-item v-if="state" label="验证码">
            <el-col :span="12">
            <el-input v-model="form.user_verify" 
              placeholder="请输入验证码">
            </el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="form.user_pwd" 
            placeholder="请输入密码" 
            show-password>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click.prevent="onSubmit" plain>{{stateName}}</el-button>
            <el-button @click.prevent="clearForm" plain>清空</el-button>
          </el-form-item>
        </el-form>

      </el-card>
      </el-col>
    </el-row>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials=true;

export default {
  name:'User',
  data(){
    return {
      state:0, // 0--登录, 1--注册
      form: {
        user_name:'',
        user_pwd:'',
        user_email:'',
        user_verify:''

      }
    }
  },
  methods:{
    clearForm(){
      this.form.user_name = ''
      this.form.user_pwd = ''
      this.form.user_email = ''
      this.form.user_verify = ''
    },
    chgState(){//注册和登录进行切换
      this.state = (this.state+1)%2
    },
    isEmail(){
      var reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
      return reg.test(this.form.user_email);
    },
    getVerify(){
      //检查邮箱格式是否正确
      if(!this.isEmail()){
        this.$message.error('邮箱错误，请重新填写...');
        return;
      }
      //发送验证码请求
      let myData = {'user_email':this.form.user_email}
      console.log('get_verifield data:', myData)
      axios.post(this.$store.state.host+"/users/verify", myData).then(
        (response) => {
          console.log("users/verify : 请求成功了", response.data);
          this.$message('验证码发送成功！');
        },
        (error)=> {
          console.log("users/verify : 请求失败了", error.message);
          this.$message.error('验证码发送失败，请重试');
        }
      )
    },
    onSubmit(){
      console.log('test')
      if(this.state == 0){ // 登录
        let myData = {'user_info':this.form.user_name, 'user_pwd':this.form.user_pwd}
        console.log('users/login Data:', myData)
        axios.post(this.$store.state.host+"/users/login", myData).then(
          (response) => {
            console.log("users/login : 请求成功了", response.data)
            // 将user_id保存至浏览器
            sessionStorage.setItem('user_id', String(response.data['user_id']))
            sessionStorage.setItem('user_name', String(response.data['user_name']))
            //sessionStorage.setItem('user_is_admin', response.data['user_is_admin']?'1':'0')
            // 将user信息保存至vuex
            let myUser = {'name':String(response.data['user_name']), 
                          'id':response.data['user_id']
                          }
            this.$store.commit('SETUSER', myUser)
            this.$store.commit('SETLOGIN',  true)
            // 显示提示
            this.$message({
              message: String(response.data['user_name']) + '，登录成功',
              type: 'success'
            })
            this.$router.push({name:'PageHome'});//待改进
          },
          (error) => {
            console.log("users/login : 请求失败了", error.message);
            this.$message.error('登录失败，请重试')
          }
        )
      }else{ // 注册
        console.log('users/signup Data:', this.form)
        axios.post(this.$store.state.host+"/users/signup", this.form).then(
          (response) => {
            console.log("users/signup : 请求成功了", response.data);
            this.$message({
              message: String(response.data['user_name']) + '，注册成功',
              type: 'success'
            });
          },
          (error) => {
            console.log("users/signup : 请求失败了", error.message);
            this.$message.error('注册失败，请重试');
          }
        )
      }
    }
  },
  computed:{
    stateName(){
      return (this.state)?"注册":"登录"
    },
    toStateName(){
      return (this.state)?"登录":"注册"
    },
    cardColor(){
      return (this.state)?"#F2F2F2":"white"
    }
  }
}
</script>

<style>

</style>