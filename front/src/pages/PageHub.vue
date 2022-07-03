<template>
<div id="#Hub">
  <div class="container" style="margin-bottom:3%;">
    <el-row :gutter="15" style="margin-top:2%;">
      <el-col :span="10" :offset="7">    
        <el-input maxlength="100" 
          placeholder="请输入内容" 
          v-model="input" 
          class="input-with-select gradient-border">
          <el-select v-model="select" slot="prepend" placeholder="请选择">
            <el-option label="植物名称" value="1"></el-option>
            <el-option label="植物属性" value="2"></el-option>
          </el-select>
          <el-button @click="searchPlant" slot="append" icon="el-icon-search" ></el-button>
        </el-input>
      </el-col>
      <el-col :span="4">
        <el-button @click="clickAddPlant" type="text">没有您想要的？点击添加植物</el-button>
      </el-col>
    </el-row>
  </div>
  <div class="container-card">
    <Card v-for="(p,index) in plants" :key="p.plant_id"
      @click.native="openPlantCard($event, index)"
      :data-image="p.src">
      <h1 slot="header">{{p.plant_name}}</h1>
      <p slot="content">{{p.plant_attr.length>20?p.plant_attr.substr(0,20)+"...":p.plant_attr}}</p>
    </Card>
  </div>
  <div class="paginate">
    <el-pagination
      ref="page"
      background
      layout="prev, pager, next"
      @current-change="handleCurrentChange"
      :page-size="pageSize"
      :total="pageTotal">
    </el-pagination>
  </div>
  <el-dialog title="植物卡片" :visible.sync="dialogVisible">
    <el-descriptions :title="dialogPlantData.plant_name" :column="1"  border >
        <el-descriptions-item label="植物介绍">{{dialogPlantData.plant_attr}}</el-descriptions-item>
        <el-descriptions-item label="百科链接"> 
          <a  target="_blank" :href="dialogPlantData.plant_src" >
            <span class="a-inner"  ><i class="el-icon-document"></i> 植物百科链接</span>
          </a>
        </el-descriptions-item>
    </el-descriptions>
    <el-image 
      v-for="(imgsrc,index) in dialogImgSrcList" :key="index"
      style= "width: 100px; height: 100px"
      :src="imgsrc"
      :preview-src-list="dialogImgSrcList">
    </el-image>
  </el-dialog>
  <el-drawer
    title="提交该地图点的维护信息"
    :visible.sync="drawerVisible"
    direction="ltr"
    custom-class="demo-drawer"
    ref="drawer"
    >
    <div class="demo-drawer__content">
      <el-form :model="addPlantForm" label-width="80px" style="margin-right:40px;margin-left:10px;">
        <el-form-item label="植物名称" >
          <el-input maxlength="100" v-model="addPlantForm.name"></el-input>
        </el-form-item>
        <el-form-item label="植物描述" >
          <el-input maxlength="200" type="text" v-model="addPlantForm.attr"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="warning" @click="submitAddPlant" plain icon="el-icon-check" >添加植物</el-button>
        </el-form-item>
      </el-form>
      <el-result v-show="showAddPlantResult" 
                :icon="resultAddPlant.icon" 
                :title="resultAddPlant.title" 
                :subTitle="resultAddPlant.content">
        <template slot="extra">
          <el-descriptions v-show="isAddPlantSuccess" :column="1"  border>
              <el-descriptions-item label="学名">{{addPlantForm.canonical_name + " " + addPlantForm.species_c}}</el-descriptions-item>
              <el-descriptions-item label="属名">{{addPlantForm.genus + ' ' + addPlantForm.genus_c}}</el-descriptions-item>
              <el-descriptions-item label="种名">{{addPlantForm.species + ' ' + addPlantForm.species_c}}</el-descriptions-item>
          </el-descriptions>
        </template>
      </el-result>
    </div>
  </el-drawer>
</div>
</template>

<script>
import Card from '../components/Card.vue'
import axios from "axios";
axios.defaults.withCredentials=true;

export default {
  data(){
    return{
      input:'',
      select:'1',
      plants:[],
      pageTotal:0,
      pageSize:10,
      dialogVisible:false,
      dialogImgSrcList:[],
      dialogPlantData:{plant_id:'', plant_name:'', plant_attr:'', plant_src:''},
      drawerVisible:false,
      addPlantForm:{name:'',attr:'',canonical_name:'', genus:'', genus_c:'', species:'', species_c:''},
      resultAddPlant:{msg:'ok', icon:'success', title:'植物添加成功', content:'植物信息如下'},
      showAddPlantResult:0,
      isAddPlantSuccess:0
    }
  },
  components:{
    Card
  },
  mounted(){
    let param = {'page_index':1, 'page_size':this.pageSize};
    axios.post(this.$store.state.host + '/plants/page', param).then(
      response => {
        if(response.data.msg == 'ok'){
          console.log('/plants/page 接口请求成功', response.data);
          this.pageTotal = response.data.total;
          let plst = response.data.data;
          for(let i = 0, len = plst.length; i < len; ++i){
            this.plants.push({  'plant_id':plst[i].plant_id,
                                'plant_name':plst[i].plant_name, 
                                'plant_attr':plst[i].plant_attr, 
                                'src':'https://picsum.photos/200/300?random='+plst[i].plant_id
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
    //向植物仓库中添加植物
    clickAddPlant(){
      //检查用户是否登录
      if(this.$store.state.login == false){
        this.$message('用户未登录');
        return;
      }
      this.addPlantForm.name='';
      this.addPlantForm.attr='';
      this.addPlantForm.canonical_name='';
      this.addPlantForm.genus='';
      this.addPlantForm.genus_c='';
      this.addPlantForm.species='';
      this.addPlantForm.species_c='';
      this.showAddPlantResult=0;
      this.isAddPlantSuccess=0;
      this.drawerVisible = true;
    },
    submitAddPlant(){
      let param = {'plant_name':this.addPlantForm.name, 'plant_attr':this.addPlantForm.attr};
      axios.post(this.$store.state.host + '/plants/check/add_plant', param).then(
        response => {
          console.log('/plants/check/add_plant 接口请求成功', response.data);
          // 添加成功
          if(response.data.msg == 'ok'){
            // addPlantForm
            this.addPlantForm.canonical_name = response.data.data['canonical_name'];
            this.addPlantForm.genus = response.data.data['genus'];
            this.addPlantForm.genus_c = response.data.data['genus_c'];
            this.addPlantForm.species = response.data.data['species'];
            this.addPlantForm.species_c = response.data.data['species_c'];
            // resultAddPlant
            this.resultAddPlant.msg='ok';
            this.resultAddPlant.icon='success';
            this.resultAddPlant.title='植物添加成功';
            this.resultAddPlant.content='植物信息如下';
            // is-show flag
            this.showAddPlantResult = 1;
            this.isAddPlantSuccess = 1;
          }
          // 添加失败（AllPlant中无该植物）
          else if(response.data.msg == 'fail'){
            // resultAddPlant
            this.resultAddPlant.msg='fail';
            this.resultAddPlant.icon='wrong';
            this.resultAddPlant.title='植物添加失败';
            this.resultAddPlant.content='数据库中未收录该植物，请使用植物种名';
            // is-show flag
            this.showAddPlantResult = 1;
            this.isAddPlantSuccess = 0;
          }
          // 添加失败（重复的植物）
          else if(response.data.msg == 're_add'){
            // addPlantForm
            this.addPlantForm.canonical_name = response.data.data['canonical_name'];
            this.addPlantForm.genus = response.data.data['genus'];
            this.addPlantForm.genus_c = response.data.data['genus_c'];
            this.addPlantForm.species = response.data.data['species'];
            this.addPlantForm.species_c = response.data.data['species_c'];
            // resultAddPlant
            this.resultAddPlant.msg='re_add';
            this.resultAddPlant.icon='warning';
            this.resultAddPlant.title='植物已存在仓库';
            this.resultAddPlant.content='植物信息如下';
            // is-show flag
            this.showAddPlantResult = 1;
            this.isAddPlantSuccess = 1;
          }
        },
        error => {
          console.log('/plants/check/add_plant 接口请求失败', error.response);
          this.$message('提交植物信息失败');
        }
      )
    },
    // 当前页变化，向后端请求数据
    handleCurrentChange(val){
      console.log('handleCurrentChange:', val);
      this.plants.splice(0);
      let param = {'page_index':val, 'page_size':this.pageSize};
      axios.post(this.$store.state.host + '/plants/page', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/plants/page 接口请求成功', response.data);
            this.pageTotal = response.data.total;
            let plst = response.data.data;
            for(let i = 0, len = plst.length; i < len; ++i){
              this.plants.push({'plant_id':plst[i].plant_id,
                                  'plant_name':plst[i].plant_name, 
                                  'plant_attr':plst[i].plant_attr, 
                                  'src':'https://picsum.photos/200/300?random='+plst[i].plant_id
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
    // 对plants中的数据进行模糊匹配
    searchPlant(){
      if(this.select !== "1" && this.select !== "2")
        return;
      this.plants.splice(0);
      let param = {'search_type':this.select, 'search_keyword':this.input}
      console.log('searchPlant:', this.input, ' select:', this.select);
      axios.post(this.$store.state.host + '/plants/search', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/plants/search 接口请求成功', response.data);
            let plst = response.data.data;
            for(let i = 0, len = plst.length; i < len; ++i){
              this.plants.push({'plant_id':plst[i].plant_id,
                                  'plant_name':plst[i].plant_name, 
                                  'plant_attr':plst[i].plant_attr, 
                                  'src':'https://picsum.photos/200/300?random='+plst[i].plant_id
                                })
            }
            this.$message({message: '搜索成功', type: 'success'});
          }
        },
        error => {
          console.log('/plants/search 接口请求失败', error.response);
          this.$message('搜索失败');
        }
      )
    },
    openPlantCard($event, index){
      // this.$message('您打开了第'+index+'个植物');
      // 设置dialogData数据
      this.dialogImgSrcList.splice(0);
      this.dialogPlantData.plant_id = this.plants[index].plant_id;
      this.dialogPlantData.plant_name = this.plants[index].plant_name;
      this.dialogPlantData.plant_attr = this.plants[index].plant_attr;
      this.dialogPlantData.plant_src = "https://www.plantplus.cn/cn/sp/" + this.plants[index].plant_name;
      // 设置可见性
      this.dialogVisible = true;

    }
  }
}
</script>

<style scoped>

.gradient-border {
  --borderWidth: 3px;
  background: #1D1F20;
  position: relative;
  border-radius: var(--borderWidth);
}
.gradient-border:after {
  content: '';
  position: absolute;
  top: calc(-1 * var(--borderWidth));
  left: calc(-1 * var(--borderWidth));
  height: calc(100% + var(--borderWidth) * 2);
  width: calc(100% + var(--borderWidth) * 2);
  background: linear-gradient(60deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
  border-radius: calc(2 * var(--borderWidth));
  z-index: -1;
  animation: animatedgradient 3s ease alternate infinite;
  background-size: 300% 300%;
}

@keyframes animatedgradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}

p {
  line-height: 1.5em;
}

h1 + p, p + p {
  margin-top: 10px;
}

.container-card {
  padding: 30px 60px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.paginate {
    position: fixed;
    bottom: 16px;
}

.el-select {
  width: 120px;
}

</style>
