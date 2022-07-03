<template>
<div id="#map">
  <el-container style="height:90vh">
    <!-- 百度地图 -->
    <el-main>
      <div 
      style="height: 100%; width: 100%; position: relative;" ref="chart"></div>
    </el-main>
    <!-- 操控面板 -->
    <el-aside style="height: 100%; width: 30%;">

      <el-alert
        title="使用说明书"
        type="success"
        description="游览模式，点击地图中已有的植物点，您将看到详细信息；编辑模式，点击地图中任意一点，您可以为它添加植物点。">
      </el-alert>

      <el-tabs type="border-card" style="margin-top:20px;">
        <el-tab-pane>
          <span slot="label"><i class="el-icon-view"></i> 游览模式</span>
          <el-descriptions :column="2"  class="margin-top" title="点击左侧地图中的植物点" border>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  经度
                </template>
                <el-tag size="small">
                {{(this.cur_point)?this.cur_point[0].value[0].toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  纬度
                </template>
                <el-tag size="small">
                {{(this.cur_point)?this.cur_point[0].value[1].toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="植物名称">紫叶李</el-descriptions-item>
              <el-descriptions-item label="植物数量">3</el-descriptions-item>
          </el-descriptions>          
          
          <!-- 图片显示 -->
          <div class="demo-image__preview" style="margin-top:20px;">
            <div class="block" style="margin:5px;">
              <el-image 
                style="width: 100px; height: 100px"
                src="https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg" 
                :preview-src-list="srcList">
              </el-image>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane>
          <span slot="label"><i class="el-icon-edit"></i> 编辑模式</span>
          <!-- 经纬度信息 -->
          <el-descriptions class="margin-top" title="添加植物点信息" border>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  经度
                </template>
                <el-tag size="small">
                {{(this.cur_point)?this.cur_point[0].value[0].toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-location"></i>
                  纬度
                </template>
                <el-tag size="small">
                {{(this.cur_point)?this.cur_point[0].value[1].toFixed(3):'未选择'}}
                </el-tag>
              </el-descriptions-item>
          </el-descriptions>
          <!-- 添加植物的表单 -->
          <el-form ref="form" label-width="80px" style="margin-top:25px;">
            <el-form-item label="植物名称">
              <el-autocomplete
                v-model="addInfo.map_plant_name"
                :fetch-suggestions="querySearchAsync"
                placeholder="请输入上传的植物名称"
                @select="handleSelect"
              ></el-autocomplete>
              <el-button style="margin-left:8px;" type="primary">从植物仓库选择</el-button>
            </el-form-item>
            <el-form-item label="植物数量">
              <el-input-number v-model="addInfo.map_plant_num" :min="1" :max="100" label="植物数量"></el-input-number>
            </el-form-item>
            <el-form-item label="图片上传">
              <el-upload
                class="upload-demo"
                action="https://jsonplaceholder.typicode.com/posts/"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :file-list="imageList"
                :auto-upload="false"
                :limit="5"
                drag multiple 
                with-credentials
                list-type="picture">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将图片拖到此处，或<em>点击上传</em></div>
                <!-- <el-button style="margin-left:8px;" size="small" type="warning">上传到服务器</el-button> -->
                <div slot="tip" class="el-upload__tip">最多5张图片，只能上传jpg/png文件，且不超过500kb</div>
              </el-upload>
            </el-form-item>
            <el-form-item>
              <el-button type="warning" @click="submitMapPoint" plain  icon="el-icon-check" >创建植物地图点</el-button>
            </el-form-item>
          </el-form>
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
        addInfo:{map_plant_id:'',map_plant_name:'', map_longitude:'', map_latitude:'', map_plant_num:1},
        // 地图上的数据
        mapdata:  [],
        plantList:[],
        srcList:  [],
        imageList: []
      }
    },
    mounted() { 
      // 初始化地图
      this.mapinit();
      // 为bmap添加点击事件监听
      this.bmap = this.chart.getModel().getComponent('bmap').getBMap();
      this.bmap.addEventListener("click",(e)=>{
        // 当前坐标赋值
        this.cur_point = [{value:[e.point.lng, e.point.lat]}]
        // 设为series数据
        this.chart.setOption({
          series:[{id:'cur_point', data:this.cur_point,}]
        })
      });
    },
    activated(){
      console.log("PageMappri 被激活了！");
      // 更新地图
      this.getmap();    
    },
    methods: {
      // 向后端请求地图点数据并加入bmap
      getmap() {
        axios.get(this.$store.state.host + '/maps/userpoints').then(
            response => {
              console.log('/maps/userpoints 请求成功了',response.data)
              if(response.data.msg == 'ok'){
                this.$message('获取地图点成功')
                // 开始解析数据: 1. 放入bmap; 2. 放入data        
                var bmap_data = []
                for(let i = 0, len = response.data.map.length; i < len; i++){
                  this.data.mapdata.push(map[i]);
                  bmap_data.push({'name':map[i].map_plant_name, 'value':[parseFloat(map[i].map_longitude),parseFloat(map[i].map_latitude), map[i].map_plant_num], 'index':map[i].map_id});
                }
                this.chart.setOption({
                  series:[{id:'map_point', data:bmap_data}]
                })
                // 绑定数据图标交互响应
              }
            },
            error => {
              console.log('/maps/userpoints 请求失败了', error.response)
              if(error.response.status == 403 ){
                this.$message('获取地图点失败：'+error.response.data.msg)
                this.$router.replace({name:'Login'})
              }
            }
          )
      },
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
      //点击出现搜索后点击的每一项
      handleSelect(item) {
        this.addInfo.map_plant_id = item.id
        this.addInfo.map_plant_name = item.value
      },
      handleRemove(image, imageList) {
        console.log(image, imageList);
      },
      handlePreview(image) {
        console.log(image);
      },
      submitMapPoint(){

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
                {name:'松树', value:[121.221152,31.29185, 3], index:'1'},
                {name:'松树', value:[121.221152,31.29000, 3]},
                {name:'松树', value:[121.221152,31.29005, 3]},
                {name:'松树', value:[121.221152,31.29085, 3]},
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

<style>

</style>