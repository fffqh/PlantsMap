<template>
<div id="#map">
  <el-container style="height:90vh">
    <!-- 百度地图 -->
    <el-main>
      <div id="box" class="gradient-border"
      style="height: 100%; width: 100%; position: relative;" ref="chart"></div>
    </el-main>
    <!-- 操控面板 -->
    <el-aside style="height: 100%; width: 30%;">

      <el-alert style="margin-top:20px;"
        title="使用说明书"
        type="success"
        description="游览模式，点击地图中已有的植物点，您将看到详细信息。私人地图不提供编辑模式。">
      </el-alert>

      <el-tabs v-model="activeTabName" @tab-click="clickTabPage" type="border-card" style="margin-top:20px;">
        <el-tab-pane name="view">
          <span slot="label"><i class="el-icon-view"></i> 游览模式</span>
          <el-descriptions :column="2"  class="margin-top" title="点击左侧地图中的植物点" border>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  经度
                </template>
                <el-tag size="small">
                {{(this.sltInfo.map_longitude)?this.sltInfo.map_longitude.toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  纬度
                </template>
                <el-tag size="small">
                {{(this.sltInfo.map_latitude)?this.sltInfo.map_latitude.toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="植物名称">{{this.sltInfo.map_plant_name}}</el-descriptions-item>
              <el-descriptions-item label="植物数量">{{this.sltInfo.map_plant_num}}</el-descriptions-item>
          </el-descriptions>          
          
          <!-- 图片显示 -->
          <div class="demo-image__preview" style="margin-top:20px;">
            <!-- <div class="block" style="margin:5px;"> -->
            <!-- </div> -->
            <div class="block" style="margin:5px;">
              <el-image  v-for="(imgsrc,index) in imageSrcList" :key="index"
                style="width: 100px; height: 100px"
                :src="imgsrc" 
                :preview-src-list="imageSrcList">
              </el-image>
            </div>
          </div>
          <!-- 历史维护记录展示 -->
          <div class="block" style="margin-top:20px;">
            <el-timeline>
              <el-timeline-item
                v-for="(mnt, index) in sltMntList"
                :key="index"
                :icon="mnt.icon"
                :type="mnt.type"
                :color="mnt.color"
                :size="mnt.size"
                :timestamp="mnt.time">
                {{mnt.title}}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-tab-pane>
      </el-tabs>      
    </el-aside>
  </el-container>
</div>
</template>

<script>

// echart的引入
import * as echarts from 'echarts/core';
import 'echarts/extension/bmap/bmap'
import {BarChart, PieChart} from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DatasetComponent
} from 'echarts/components';
echarts.use(
  [
    TitleComponent,
    TooltipComponent,
    GridComponent,
    BarChart,
    PieChart,
    LegendComponent,
    DatasetComponent,
    CanvasRenderer
  ]
);

// axios的引入
import axios from "axios";
axios.defaults.withCredentials=true;


export default {
    data() { 
      return { 
        chart: null, //echart图表实例 
        bmap:null,   //百度地图实例
        cur_point:null, //当前鼠标的坐标
        activeTabName:'view', //当前活跃的Tab页面名称
        addInfo:{ map_plant_id:'',
                  map_plant_name:'', 
                  map_longitude:'', 
                  map_latitude:'', 
                  map_plant_num:1},
        //上传图片表单数据
        uploadImgData:{map_id:null},
        uploadImgDataMnt:{msg_id:null},
        imageList:   [],
        imageListMnt:[],
        sltInfo:{ map_id:null, 
                  map_user_id:null,
                  map_plant_name:'', 
                  map_longitude:null, 
                  map_latitude:null, 
                  map_plant_num:null},
        sltMntList:[],
        // 地图上的数据
        mapdata:  [],
        plantList:[],
        imageSrcList: [],
        imageIdList:[],
        dialog: false,
        mntForm: {
          mnt_type:null,
          mnt_desc:''
        },
      }
    },
    mounted() { 
      // 初始化地图
      this.mapinit();
      // 为bmap添加点击事件监听
      this.bmap = this.chart.getModel().getComponent('bmap').getBMap();
      // this.bmap.addEventListener("click",(e)=>{
      //   // 当前坐标赋值
      //   this.cur_point = [{value:[e.point.lng, e.point.lat]}]
      //   // 设为series数据
      //   this.chart.setOption({
      //     series:[{id:'cur_point', data:this.cur_point,}]
      //   })
      // });
      // 为echart添加点击事件监听
      this.chart.on('click', (params)=>{
        console.log('echarts click:', params);
        if(params.seriesName == "当前位置"){
          return;
        }
        this.sltInfo.map_longitude = parseFloat(params.value[0]);
        this.sltInfo.map_latitude = parseFloat(params.value[1]);
        this.sltInfo.map_id = params.data.index;
        this.sltInfo.map_user_id = params.data.map_user_id;
        this.sltInfo.map_plant_name = params.name;
        this.sltInfo.map_plant_num = params.value[2];
        this.getmapimgs();
        this.getmapmnts();
      })
    },
    activated(){
      console.log("PageMappub 被激活了！");
      // 更新地图
      this.getmap();
    },
    methods: {
      dialogOpen(){
        if(this.$store.state.login == false){
          this.$message('用户未登录，无法使用通信箱功能');
          return;
        }
        this.dialog=true;
      },
      clickTabPage(){
        if(this.activeTabName == 'view'){
          this.$notify({
            title: '游览模式',
            message: '您可以点击图中的绿色标记来查看植物信息',
            position: 'bottom-left'
          });
        }else{
          // 检查是否已经登录
          if(this.$store.state.login == false){
            this.$router.replace({name:'Login'});
            this.$message('用户未登录');
            return;
          }
          this.$notify({
            title: '编辑模式',
            message: '您可以点击图中的任意一点来添加信息',
            position: 'bottom-right'
          });
        }
      },
      // 向后端请求sltInfo地图点的图片
      getmapimgs(){
        console.log('getmapimgs函数被调用');
        // 清空原有数据
        this.imageIdList.splice(0);
        this.imageSrcList.splice(0);
        // 发送网络请求
        let param = {map_id:this.sltInfo.map_id};
        axios.post(this.$store.state.host + '/images/get_mapimgs', param).then(
          response => {
            if(response.data.msg == 'ok'){
              console.log('/images/get_mapimgs 接口调用成功', response.data);
              let idlst = response.data.images_id
              for(let i = 0, len =idlst.length; i < len; ++i){
                this.imageIdList.push(idlst[i]);
                this.imageSrcList.push(this.$store.state.host + '/images/' + idlst[i].toString());
              }
            }
          },
          error => {
            console.log('/images/get_mapimgs 接口调用失败', error.response);
            this.$message('获取图片失败');
          }
        )
      },
      // 向后端请求sltInfo地图点的历史维护信息
      getmapmnts(){
        this.sltMntList.splice(0);
        let param = {'map_id': this.sltInfo.map_id}
        axios.post(this.$store.state.host+'/maps/mnts', param).then(
          response => {
            if(response.data.msg == 'ok'){
              console.log('/maps/mnts 接口调用成功', response.data);
              let mnt_list = response.data.mnts;
              for(let i = 0, len = mnt_list.length; i < len; ++i){
                let title = mnt_list[i].mnt_type + '用户：' + mnt_list[i].mnt_user_name;
                let time = mnt_list[i].mnt_time;
                let color = mnt_list[i].mnt_type == '创建'? "#0bbd87":"	#FFD700";
                this.sltMntList.push({'title':title, 'time':time, 'color':color});
              }
            }
          },
          error => {
            consele.log('/maps/mnts 接口调用失败', error.response);
            this.$message('获取历史维护信息失败');
          }
        )
      },
      // 向后端请求地图点数据并加入bmap
      getmap() {
        console.log("get userpoints url:",this.$store.state.host+'/maps/userpoints')
        axios.get(this.$store.state.host+'/maps/userpoints').then(
          response => {
            console.log('/maps/userpoints 请求成功了',response.data)
            if(response.data.msg == 'ok'){
              this.$message('获取地图点成功')
              // 开始解析数据: 1. 放入bmap; 2. 放入data        
              var bmap_data = []
              console.log(response.data);
              for(let i = 0, len = response.data.map.length; i < len; i++){
                this.mapdata.push(response.data.map[i]);
                bmap_data.push({'name':response.data.map[i].map_plant_name, 
                                'map_user_id':response.data.map_user_id,
                                'map_plant_id':response.data.map_plant_id,
                                'value':[parseFloat(response.data.map[i].map_longitude),parseFloat(response.data.map[i].map_latitude), response.data.map[i].map_plant_num],
                                'index':response.data.map[i].map_id});
              }
              this.chart.setOption({
                series:[{id:'map_point', data:bmap_data}]
              })
              // 绑定数据图标交互响应
            }
          },
          error => {
            console.log('/maps/userpoints 请求失败了', error.response)
            this.$message('获取地图点失败')
          }
        )
      },
      //input remote 钩子函数
      querySearchAsync(queryString, cb) {
        //清空定时器
        clearTimeout(this.timeout);
        //准备result数组
        let results = []
        if (queryString == '') {
          cb(results);
        } else {
          //准备接口需要的参数
          let find = {
            keyword: queryString//上面输入框绑定的数据
          };
          //这里去掉后端的接口.根据自己接口的情况进行赋值
          axios.post(this.$store.state.host + "/plants/search_plant", find).then(
            response => {
              if (response.data.msg == 'ok') {
                let result = response.data.result
                //循环放到一个远程搜索需要的数组
                for (let i = 0; i < result.length; i++) {
                  const element = result[i];
                  results.push({
                    value: element.plant_name,
                    id: element.plant_id
                  })
                }
                cb(results);
              } else {
                results = []
                cb(results);
              }
            },
            error => {
              console.log('/plants/search_plant 请求失败了', error.response)
            }
          );
        }
      },
      //drawer 钩子函数
      handleDrawerClose(done) {
        this.imageListMnt.splice(0);
        done();
      },
      //input remote 钩子函数
      handleSelect(item) {
        this.addInfo.map_plant_id = item.id
        this.addInfo.map_plant_name = item.value
      },
      //upload钩子函数
      handleChange(image, imageList) { //文件数量改变
        console.log('handleChange:', image, imageList);
        this.imageList = imageList;
      },
      handleChangeMnt(image, imageList){
        console.log('handleChange:', image, imageList);
        this.imageListMnt = imageList;
      },
      //upload钩子函数
      handleRemove(image, imageList) {
        console.log('handleRemove:', image, imageList);
      },
      //upload钩子函数
      handlePreview(image) {
        console.log('handlePreview:', image);
      },
      //upload钩子函数
      handleError(err, image, imageList) {
        this.$message('图片上传失败');
      },
      //提交地图点
      submitMapPoint(){
        if(this.cur_point === null){
          this.$message('请在地图中选择坐标后再进行提交')
          return;
        }
        this.addInfo.map_longitude = this.cur_point[0].value[0];
        this.addInfo.map_latitude = this.cur_point[0].value[1];
        console.log('addpoint:', this.addInfo);
        axios.post(this.$store.state.host+"/maps/addpoint", this.addInfo).then(
            response => {
              if (response.data.msg == 'ok') {
                console.log('/maps/addpoint 请求成功了', response.data);
                this.uploadImgData.map_id = response.data.map_id;
                //console.log(this.uplaodImgData);
                this.$message( {message: '地图点提交成功', type: 'success'});
                // 发送图片提交请求
                this.$refs.upload.submit();
                // 更新地图
                this.getmap();
              }
            },
            error => {
              console.log('/maps/addpoint 请求失败了', error.response);
              this.$message('提交地图点失败:');
            }
        )
      },
      submitMntInfo() {
        if(this.cur_point === null){
          this.$message('请在地图中选择坐标后再进行提交')
          return;
        }
        let param = {'map_id':this.sltInfo.map_id, 'mnt_type':this.mntForm.mnt_type, 'mnt_desc':this.mntForm.mnt_desc};
        axios.post(this.$store.state.host+"/message/addmsg", param).then(
            response => {
              if (response.data.msg == 'ok') {
                console.log('/message/addmsg 请求成功了', response.data);
                this.uploadImgDataMnt.msg_id = response.data.msg_id;
                this.$message( {message: '维护请求提交成功', type: 'success'});
                // 发送图片提交请求
                this.$refs.uploadmnt.submit();
              }
            },
            error => {
              console.log('/message/addmsg 请求失败了', error.response);
              this.$message('提交维护请求失败:');
            }
        )
      },
      //获取选择点的用户信息
      openUserInfo(){
        if(this.sltInfo.map_user_id == null){
          return;
        }
        //向后端发送请求，获取用户信息
      },
      // 地图的初始化函数，由mounted生命周期函数调用
      mapinit() {
        // 初始化echart
        this.chart = echarts.init(this.$refs.chart);
        // 为echart进行配置
        this.chart.setOption({
          backgroundColor: 'transparent',
          tooltip: {
            trigger: 'item'
          },
          // echart系列数据
          series:[
            // 当前选中的位置
            {
              name:"当前位置",
              type: 'custom',
              id:'cur_point',
              silent:true,
              coordinateSystem: 'bmap',
              data:this.cur_point,
              // 实现地图点的动画效果
              renderItem(params, api) {
                const coord = api.coord([
                  api.value(0, params.dataIndex),
                  api.value(1, params.dataIndex)
                ]);
                const circles = [];
                for (let i = 0; i < 5; i++) {
                  circles.push({
                    type: 'circle',
                    shape: {
                      cx: 0,
                      cy: 0,
                      r: 30
                    },
                    style: {
                      stroke: 'red',
                      fill: 'none',
                      lineWidth: 2
                    },
                    // Ripple animation
                    keyframeAnimation: {
                      duration: 4000,
                      loop: true,
                      delay: (-i / 4) * 4000,
                      keyframes: [
                        {
                          percent: 0,
                          scaleX: 0,
                          scaleY: 0,
                          style: {
                            opacity: 1
                          }
                        },
                        {
                          percent: 1,
                          scaleX: 1,
                          scaleY: 0.4,
                          style: {
                            opacity: 0
                          }
                        }
                      ]
                    }
                  });
                }
                return {
                  type: 'group',
                  x: coord[0],
                  y: coord[1],
                  children: [
                    ...circles,
                    {
                      type: 'path',
                      shape: {
                        d: 'M16 0c-5.523 0-10 4.477-10 10 0 10 10 22 10 22s10-12 10-22c0-5.523-4.477-10-10-10zM16 16c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z',
                        x: -10,
                        y: -35,
                        width: 20,
                        height: 40
                      },
                      style: {
                        fill: 'blue'
                      },
                      // Jump animation.
                      keyframeAnimation: {
                        duration: 1000,
                        loop: true,
                        delay: Math.random() * 1000,
                        keyframes: [
                          {
                            y: -10,
                            percent: 0.5,
                            easing: 'cubicOut'
                          },
                          {
                            y: 0,
                            percent: 1,
                            easing: 'bounceOut'
                          }
                        ]
                      }
                    }
                  ]
                };
              },
            },
            // 已有的植物点
            {
              // 这一系列坐标的名称：植物名称
              name: '植物名称',
              type: 'custom',
              id:'map_point',
              // 使用百度地图作为坐标系
              coordinateSystem: 'bmap',
              // 所有植物地图点的坐标数据、植物名称、植物数量
              data:[
                // {name:'松树', value:[121.221152,31.29185, 3]},
                // {name:'松树', value:[121.221152,31.29000, 3]},
                // {name:'松树', value:[121.221152,31.29005, 3]},
                // {name:'松树', value:[121.221152,31.29085, 3]},
              ],
              // 实现地图点的动画效果
              renderItem(params, api) {
                const coord = api.coord([
                  api.value(0, params.dataIndex),
                  api.value(1, params.dataIndex)
                ]);
                const circles = [];
                for (let i = 0; i < 5; i++) {
                  circles.push({
                    type: 'circle',
                    shape: {
                      cx: 0,
                      cy: 0,
                      r: 30
                    },
                    style: {
                      stroke: 'green',
                      fill: 'none',
                      lineWidth: 2
                    },
                    // Ripple animation
                    keyframeAnimation: {
                      duration: 4000,
                      loop: true,
                      delay: (-i / 4) * 4000,
                      keyframes: [
                        {
                          percent: 0,
                          scaleX: 0,
                          scaleY: 0,
                          style: {
                            opacity: 1
                          }
                        },
                        {
                          percent: 1,
                          scaleX: 1,
                          scaleY: 0.4,
                          style: {
                            opacity: 0
                          }
                        }
                      ]
                    }
                  });
                }
                return {
                  type: 'group',
                  x: coord[0],
                  y: coord[1],
                  children: [
                    ...circles,
                    {
                      type: 'path',
                      shape: {
                        d: 'M16 0c-5.523 0-10 4.477-10 10 0 10 10 22 10 22s10-12 10-22c0-5.523-4.477-10-10-10zM16 16c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z',
                        x: -10,
                        y: -35,
                        width: 20,
                        height: 40
                      },
                      style: {
                        fill: 'green'
                      },
                      // Jump animation.
                      keyframeAnimation: {
                        duration: 1000,
                        loop: true,
                        delay: Math.random() * 1000,
                        keyframes: [
                          {
                            y: -10,
                            percent: 0.5,
                            easing: 'cubicOut'
                          },
                          {
                            y: 0,
                            percent: 1,
                            easing: 'bounceOut'
                          }
                        ]
                      }
                    }
                  ]
                };
              },
              // 将value的维度3，作为label显示的数据（表示植物数量）
              encode:{
                value:2
              }
            }
          ],
          // 百度地图 API 配置项
          bmap:{
            center: [121.2199, 31.2914],
            zoom: 17,
            roam: true,
            mapStyle: {
              styleJson:
              [{
                  "featureType": "land",
                  "elementType": "geometry",
                  "stylers": {
                      "color": "#fffff9ff"
                  }
              }, {
                  "featureType": "water",
                  "elementType": "geometry",
                  "stylers": {
                      "color": "#69b0acff"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#94ad79ff"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "arterial",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#d4e2c6ff"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#d4e2c6ff"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#d4e2c6ff"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "tertiaryway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#ffffffff"
                  }
              }, {
                  "featureType": "tertiaryway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "fourlevelway",
                  "elementType": "geometry.fill",
                  "stylers": {
                      "color": "#ffffffff"
                  }
              }, {
                  "featureType": "fourlevelway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "subway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "railway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "highwaysign",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "highwaysign",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "nationalwaysign",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "nationalwaysign",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "provincialwaysign",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "provincialwaysign",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "tertiarywaysign",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "tertiarywaysign",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "subwaylabel",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "subwaylabel",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#94ad79ff"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "arterial",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#b5caa0ff"
                  }
              }, {
                  "featureType": "highway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "highway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "highway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "highway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "highway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "nationalway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "nationalway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "nationalway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "nationalway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "nationalway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "provincialway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "provincialway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "provincialway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "8,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "cityhighway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "cityhighway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "cityhighway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "cityhighway",
                  "stylers": {
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "geometry",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "6"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "7"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "8"
                  }
              }, {
                  "featureType": "cityhighway",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off",
                      "curZoomRegionId": "0",
                      "curZoomRegion": "6,9",
                      "level": "9"
                  }
              }, {
                  "featureType": "entertainment",
                  "elementType": "geometry",
                  "stylers": {
                      "color": "#e4f0d7ff"
                  }
              }, {
                  "featureType": "manmade",
                  "elementType": "geometry",
                  "stylers": {
                      "color": "#effcf0ff"
                  }
              }, {
                  "featureType": "education",
                  "elementType": "geometry",
                  "stylers": {
                      "color": "#e3f7e4ff"
                  }
              }, {
                  "featureType": "building",
                  "elementType": "geometry.stroke",
                  "stylers": {
                      "color": "#a1cfa4ff"
                  }
              }, {
                  "featureType": "poilabel",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "poilabel",
                  "elementType": "labels.icon",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "education",
                  "elementType": "labels.text.fill",
                  "stylers": {
                      "color": "#7a7a7aff"
                  }
              }, {
                  "featureType": "education",
                  "elementType": "labels.text.stroke",
                  "stylers": {
                      "color": "#ffffffff"
                  }
              }, {
                  "featureType": "education",
                  "elementType": "labels.text",
                  "stylers": {
                      "fontsize": 26
                  }
              }, {
                  "featureType": "manmade",
                  "elementType": "labels.text.fill",
                  "stylers": {
                      "color": "#afafafff"
                  }
              }, {
                  "featureType": "manmade",
                  "elementType": "labels.text",
                  "stylers": {
                      "fontsize": 26
                  }
              }, {
                  "featureType": "scenicspotslabel",
                  "elementType": "labels.text.fill",
                  "stylers": {
                      "color": "#376b6dff"
                  }
              }, {
                  "featureType": "scenicspots",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "off"
                  }
              }, {
                  "featureType": "scenicspotslabel",
                  "elementType": "labels",
                  "stylers": {
                      "visibility": "on"
                  }
              }, {
                  "featureType": "scenicspotslabel",
                  "elementType": "labels.text.stroke",
                  "stylers": {
                      "color": "#ffffffff",
                      "weight": 4
                  }
              }, {
                  "featureType": "country",
                  "elementType": "labels.text.fill",
                  "stylers": {
                      "color": "#376b6dff"
                  }
              }, {
                  "featureType": "country",
                  "elementType": "labels.text.stroke",
                  "stylers": {
                      "color": "#ffffffff",
                      "weight": 3
                  }
              }, {
                  "featureType": "water",
                  "elementType": "labels.text.fill",
                  "stylers": {
                      "color": "#ffffffff"
                  }
              }, {
                  "featureType": "water",
                  "elementType": "labels.text.stroke",
                  "stylers": {
                      "color": "#ffffff00"
                  }
              }, {
                  "featureType": "water",
                  "elementType": "labels.text",
                  "stylers": {
                      "fontsize": 24
                  }
              }]
              
            }
          }
        });
      }
    }
};
</script>

<style scoped>
#box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 400px;
  height: 200px;
  color: white;
  font-family: 'Raleway';
  font-size: 2.5rem;
}
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
</style>