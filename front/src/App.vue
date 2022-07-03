<template>
  <div id="root" class="container">
    <el-row type="flex" :gutter="1" justify="space-between">
      <!-- 侧边栏 -->
      <el-col :span="isCollapse ?1:3">
        <div class="title-text">
          <span>
            <span v-show="!isCollapse">人间花木</span>
          </span>
        </div>
        <el-menu class="el-menu-vertical-demo" :collapse="isCollapse" >
          <el-menu-item index="0" @click="toIndex">
            <i class="el-icon-guide"></i>
            <span slot="title">首页</span>
          </el-menu-item>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-map-location"></i>
              <span slot="title">植物地图</span>
            </template>
            <el-menu-item index="1-1" @click="toPublicMap">
              <i class="el-icon-star-off"></i>
              <span slot="title">共享地图</span>
            </el-menu-item>
            <el-menu-item index="1-2" @click="toPrivateMap">
              <i class="el-icon-star-off"></i>
              <span slot="title">私人地图</span>
            </el-menu-item>
          </el-submenu>
          <el-menu-item index="2" @click="toHub">
            <i class="el-icon-menu"></i>
            <span slot="title">植物仓库</span>
          </el-menu-item>
          <el-menu-item index="3" @click="toMessage">
            <i class="el-icon-message"></i>
            <span slot="title">通讯箱</span>
          </el-menu-item>
          <el-menu-item index="4" @click="toHome">
            <i class="el-icon-medal"></i>
            <span slot="title">个人中心</span>
          </el-menu-item>
        </el-menu>
      </el-col>

      <el-col :span="isCollapse? 23:21">
        <!-- 头部导航栏 -->
        <el-row type="flex" justify="start" align="bottom">
          <el-col :span="2">  
            <div class="collapsBtn">
              <el-button icon="el-icon-magic-stick" 
                @click="toggleCollapse" 
                style="margin-left: 10px;"
              ></el-button>
            </div>
          </el-col>
          <el-col :span="18"></el-col>
          <el-col :span="2">
            <el-row>
              <el-col :span="12">
                <el-avatar style="margin-top:10px;" @click.native="clickUserAvatar" icon="el-icon-user-solid"></el-avatar>
              </el-col>
              <el-col :span="12">
                <el-dropdown @command="handleCommand">
                <el-button style="margin-top:10px;" class="el-dropdown-link" type="text">{{this.$store.state.user.name}}</el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="logout" icon="el-icon-switch-button">登出</el-dropdown-item>
                </el-dropdown-menu>
                </el-dropdown>
              </el-col>
            </el-row>
          </el-col>
        
        </el-row>
        <!-- 内容 -->
        <keep-alive> 
          <router-view>
          </router-view>
        </keep-alive>

      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.withCredentials=true;

import PageHome     from './pages/PageHome.vue'
import PageHub      from './pages/PageHub.vue'
import PageMappub      from './pages/PageMappub.vue'
import PageMappri      from './pages/PageMappri.vue'
import PageMessage  from './pages/PageMessage.vue'
import Index        from './pages/Index.vue'
import Login        from './pages/Login.vue'

export default {
  name: "App",
  components:{
    PageHome, PageHub, PageMappub, PageMappri, PageMessage, Index, Login
  },
  data() {
    return {
      isCollapse: true
    };
  },
  mounted(){
    // 设置背景颜色
    document.body.style.backgroundColor="#D4EEEA";
    // 同步登录状态
    axios.get(this.$store.state.host + '/users/islogin').then(
      response => {
        if(response.data.msg == 'yes'){
          sessionStorage.setItem('user_id', String(response.data.user_id));
          sessionStorage.setItem('user_name', String(response.data.user_name));
          this.$store.commit('SETUSER', {'id':response.data.user_id, 'name':response.data.user_name});
          this.$store.commit('SETLOGIN',  true);
        }
      },
      error => {
        this.$$message('账号状态同步错误，请检查接口');
      }
    )
  },
  methods: {
    handleCommand(command) {
      if(command == 'logout'){
        this.clickLogout();
      }
    },
    clickLogout(){
      axios.post(this.$store.state.host+'/users/logout').then(
        response => {
          console.log('/users/logout 接口调用成功', response.data);
          sessionStorage.removeItem('user_id');
          sessionStorage.removeItem('user_name');
          this.$store.commit('SETUSER', {'id':-1, 'name':''});
          this.$store.commit('SETLOGIN',  false);
          this.$message('登出成功!');
        },
        error => {
          console.log('/users/logout 接口调用失败', error.response);
        }
      )
    },
    // 点击用户头像按钮（1.已登录：个人中心； 2.未登录：登录界面）
    clickUserAvatar(){
      let user_id = window.sessionStorage.getItem("user_id");
      this.$message('user_id: ' + String(user_id));
      if(user_id != null){
        this.toHome();
      }else{
        this.$router.replace({name:'Login'});
      }
    },
    // 点击按钮，切换菜单的折叠与展开
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },
    // 编程式路由
    toIndex(){
      this.$router.push({name:'Index'});
    },
    toPublicMap(){
      this.$router.push({name:'PageMappub'});
    },
    toPrivateMap(){
      if(this.$store.state.login){
        this.$router.push({name:'PageMappri'});
      }else{
        this.$router.replace({name:'Login'});
        this.$message('用户未登录');
      }
    },
    toHub(){
      this.$router.replace({name:'PageHub'});
    },
    toMessage(){
      if(this.$store.state.login){
        this.$router.replace({name:'PageMessage'})
      }else{
        this.$router.replace({name:'Login'});
        this.$message('用户未登录');
      }
    },
    toHome(){
      if(this.$store.state.login){
        this.$router.replace({name:'PageHome'});
      }else{
        this.$router.replace({name:'Login'});
        this.$message('用户未登录');
      }
    }
  },
};

</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  min-width: 0px;
  /* min-height: 400px; */
}
.el-menu-vertical-demo {
  margin-top: 15px;
  border-radius:15px;
}

.title-text{
  font-family: STZhongsong;
  font-size: 130%;
  font-weight: 800;
  color:rgb(81, 194, 113);
  min-height: 40px;
  text-align: center;
  margin-top: 10px;
}

.el-submenu .el-menu-item {
    min-width: 0px;
}

/* .el-header {
  position: relative;
  width: 100%;
  height: 60px;      
} */
/* .el-aside {
  display: block;
  position: absolute;
  left: 0;
  top: 60px;
  bottom: 0;
  } */
/* .el-main {
  position: absolute;
  left: 200px;
  right: 0;
  top: 60px;
  bottom: 0;
  overflow-y: scroll;
} */


</style>
