<template>
<div id="#home">
    <el-container direction="vertical">
      <el-main>
    
        <h1>用户信息</h1>
        <el-row style="width=80%;margin-top:20px; margin-left:20px;" :gutter="20">
          <el-col :span="4" >
            <div class="pimage">
              <el-avatar :size="80" :src="portrait_img"></el-avatar>
            </div>
            <div class="message">
              <p>昵称：{{user_name}}</p>
              <p>用户ID：{{user_id}}</p>
            </div>
          </el-col>
          <el-col :span="18">
            <History></History>
          </el-col>
        </el-row>
      </el-main>
      <el-main style="width:98%;">
        <h1>拥有植物</h1>
        <el-table fit="true" :data="plants" :row-class-name="tableRowClassName">
          <el-table-column
            prop="map_plant_name"
            label="植物名"
>
          </el-table-column>
          <el-table-column
            prop="map_create_time"
            label="创建时间"
>
          </el-table-column>
          <el-table-column
            prop="map_longitude"
            label="经度"
>
          </el-table-column>
          <el-table-column
            prop="map_latitude"
            label="纬度"
>
          </el-table-column>
          <el-table-column
            prop="map_plant_num"
            label="植物数量"
>
          </el-table-column>
        </el-table>
      </el-main>
      <el-row>
          <el-pagination
            background
            layout="prev, pager, next"
            @current-change="handleCurrentChange"
            :page-size="pageSize"
            :total="pageTotal">
          </el-pagination>
      </el-row>
    </el-container>
</div>
</template>

<script>
import History from '../components/History.vue'
import axios from "axios";
axios.defaults.withCredentials=true;

export default {
    data () {
      return {
        portrait_img: "https://img1.baidu.com/it/u=581869593,2565556038&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
        user_name:'',
        user_id:'',
        plants: [],
          pageTotal:36,
          pageSize:4
        
      }
    },
    components:{
      History
    },
    activated(){
      this.user_name = window.sessionStorage.getItem('user_name');
      this.user_id = window.sessionStorage.getItem('user_id');
      console.log('user_name', this.user_name);
      console.log('user_id', this.user_id);
    },
    mounted(){
      let user_id = window.sessionStorage.getItem('user_id');
    let param = {'page_index':1, 'page_size':this.pageSize,'user_id':user_id};
    axios.post(this.$store.state.host + '/home/points', param).then(
      response => {
        if(response.data.msg == 'ok'){
          console.log('/plants/page 接口请求成功', response.data);
          this.pageTotal = response.data.total;
          let plst = response.data.data;
          for(let i = 0, len = plst.length; i < len; ++i){
            this.plants.push({'map_id':plst[i].map_id,
                                'map_plant_id':plst[i].map_plant_id,
                                'map_plant_name':plst[i].map_plant_name,
                                'map_create_time':plst[i].map_create_time,
                                'map_update_time':plst[i].map_update_time,
                                'map_longitude':parseFloat(plst[i].map_longitude).toFixed(4),
                                'map_latitude':parseFloat(plst[i].map_latitude).toFixed(4),
                                'map_plant_num':plst[i].map_plant_num

                              })
          }
          this.$message({message: '获取植物信息成功', type: 'success'});
        }
      },
      error => {
        console.log('/plants/page 接口请求失败', error.response);
        this.$message('获取植物信息失败');
      }
    )
    },
    methods: {
      tableRowClassName({row, rowIndex}) {
        if (rowIndex%2 == 1) {
          return 'warning-row';
        } else {
          return 'success-row';
        }
      },
      handleCurrentChange(val){
      console.log('handleCurrentChange:', val);
      this.plants.splice(0);
      console.log(this.$store.state);
      let user_id = window.sessionStorage.getItem('user_id');
      let param = {'page_index':val, 'page_size':this.pageSize,'user_id':user_id};
      axios.post(this.$store.state.host + '/home/points', param).then(
      response => {
        if(response.data.msg == 'ok'){
          console.log('/plants/page 接口请求成功', response.data);
          this.pageTotal = response.data.total;
          let plst = response.data.data;
          for(let i = 0, len = plst.length; i < len; ++i){
            this.plants.push({'map_id':plst[i].map_id,
                                'map_plant_id':plst[i].map_plant_id,
                                'map_plant_name':plst[i].map_plant_name,
                                'map_create_time':plst[i].map_create_time,
                                'map_update_time':plst[i].map_update_time,
                                'map_longitude':parseFloat(plst[i].map_longitude).toFixed(4),
                                'map_latitude':parseFloat(plst[i].map_latitude).toFixed(4),
                                'map_plant_num':plst[i].map_plant_num

                              })
          }
          this.$message({message: '获取植物信息成功', type: 'success'});
        }
      },
      error => {
        console.log('/plants/page 接口请求失败', error.response);
        this.$message('获取植物信息失败');
      }
      )
    }





    } 
}

</script>

<style scoped>
  /* .all
  {
    border-style:solid; 
    border-width:3px; 
    border-color:#35fc35;
    background-color:rgb(146, 221, 162);
    /* background-image: url("../assets/pagehome.png"); 
  } */
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
.el-table{
  border-radius: 10px;
}

.avatar
{
    position: relative;
    left: 120px;
    top: 10px;
    height: 100px;
}

h1 {
  color:rgb(130, 207, 207);
  font-weight: 1000;
  font-size:20px;
}
.message
{
    position: relative;
    left: 100px;
    top: -85px;
    color:rgb(130, 207, 207);
}

</style>