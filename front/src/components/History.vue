<template>
  <div class="container-card">
    <ul class="graph">
      <el-tooltip
        class="item"
        effect="dark"
        :content="item.year + '-' + item.month + '-' + item.date"
        placement="top-start"
        v-for="(item, index) in infos"
        :key="index"
        :open-delay="500"
      >
        <li
          :data-level="item.level"
          class="li-day"
          :isToday="item.isToday"
          @click="handleClick(item)"
        ></li>
      </el-tooltip>
    </ul>

    <ul class="months">
      <li class="li-month" v-for="(item, index) in monthBar" :key="index">
        {{ item }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.withCredentials=true;

export default {
  data() {
    return {
      infos: [],
      current: {
        year: "",
        month: "",
        date: "",
      },
      monthBar: ["", "", "", "", "", "", "", "", "", "", "", ""],
    };
  },
  methods: {
    handleClick: function (item) {
      console.log(item.year + "-" + item.month + "-" + item.date);
      alert(item.year + "-" + item.month + "-" + item.date);
    },
  },
  created() {
    // let param = {'user_id':this.$store.state.user.id};
    // axios.post(this.$store.state.host + '/home/points', param).then(
    //   response => {
    //     if(response.data.msg == 'ok'){
    //       console.log('/plants/page 接口请求成功', response.data);
    //       this.pageTotal = response.data.total;
    //       let plst = response.data.data;
    //       for(let i = 0, len = plst.length; i < len; ++i){
    //         this.plants.push({'map_id':plst[i].map_id,
    //                             'map_plant_id':plst[i].map_plant_id,
    //                             'map_plant_name':plst[i].map_plant_name,
    //                             'map_create_time':plst[i].map_create_time,
    //                             'map_update_time':plst[i].map_update_time,
    //                             'map_longitude':plst[i].map_longitude,
    //                             'map_latitude':plst[i].map_latitude,
    //                             'map_plant_num':plst[i].map_plant_num

    //                           })
    //       }
    //       this.$message({message: '获取植物信息成功', type: 'success'});
    //     }
    //   },
    //   error => {
    //     console.log('/plants/page 接口请求失败', error.response);
    //     this.$message('获取植物信息失败');
    //   }
    // );

    let d = new Date();
    let now=new Date();
    let day = d.getDay();
    let today = d.getDate();
    let info = {};
    d.setDate(d.getDate() - 300);
    let firstday= d.getDate();
    this.current.year = d.getFullYear();
    this.current.month = d.getMonth();
    this.current.date = d.getDate();
    let month = "";
    let weekOfMonth = "";
    for (let i = 0; i < 301; i++) {
      d.setFullYear(this.current.year);
      d.setMonth(this.current.month);
      d.setDate(this.current.date);
      d.setDate(firstday +i);
      console.log(d);
      
      let level = Math.floor(Math.random() * 4);
      if (
        d.getMonth() == now.getMonth() &&
        d.getDate() == now.getDate()
      ) {
        info = {
          year: d.getFullYear(),
          month: d.getMonth() + 1,
          date: d.getDate(),
          number: 10,
          level: level,
          isToday: true,
        };
        this.infos.push(info);
      } else {
        info = {
          year: d.getFullYear(),
          month: d.getMonth() + 1,
          date: d.getDate(),
          number: 10,
          level: level,
          isToday: false,
        };
        this.infos.push(info);
      }
      if (d.getDate() == 1) {
        month = d.getMonth() + 1;
        weekOfMonth = parseInt((i ) / 7);
        this.monthBar[weekOfMonth] = month + "月";
      }
    }
  }
};
</script>

<style scoped>
.container-card {
  /* position: absolute; */
  height: 200px;
  width:950px;
  padding: 5px 5px 0px 5px;
  border: 1px solid #ebeef5;
  border-radius: 10px;
  background-color: #fff;
}
.container-card:hover {
  box-shadow: 0px 0px 5px 5px #cfcfcf;
}
.graph {
  display: grid;
  grid-template-columns: repeat(43, 21px);
  grid-template-rows: repeat(7, 21px);
  padding-inline-start: 0px;
  grid-auto-flow: column;
  margin: 20px 20px 5px 20px;
}
.months {
  display: grid;
  grid-template-columns: repeat(43, 21px);
  grid-template-rows: 21px;
  font-size: 8px;
  color: #aaa;
  padding-inline-start: 0px;
  margin: 5px 20px 5px 20px;
}
.li-month {
  display: inline-block;
  width:30px;
}
.li-day {
  background-color: #eaeaea;
  list-style: none;
  border-radius: 3px;
}
.li-day:hover {
  box-shadow: 0px 0px 5px rgb(57, 120, 255);
}
.li-day[isToday="true"] {
  background-color: rgb(234, 234, 234);
  box-shadow: 0px 0px 5px red;/*rgb(57, 120, 255);*/
  list-style: none;
  border-radius: 3px;
}
.graph li[data-level="1"] {
  background-color: hsl(131, 58%, 82%);
}
.graph li[data-level="2"] {
  background-color: #6eec83;
}
.graph li[data-level="3"] {
  background-color: #0a8830;
}
.item {
  margin: 2.5px;
}
</style>

