<template>
<div id="#message">
<el-container style="height:90vh; " >
  <el-main style="height:100%;width:50%;">
    <div class="conic" style="height:81vh;" >
        <el-divider content-position="left">收件箱</el-divider>
        <div v-for="(msg, index) in recvMsg" :key="index" class="card card-1" @click="clickMsg($event, msg)">
          <h3>{{msg.msgTitle}}</h3>
          <p>{{msg.msgPre}}</p>
        </div>
        <el-pagination
          ref="recvPage"
          background
          layout="prev, pager, next"
          @current-change="recvCurrentChange"
          :page-size="pageSize"
          :total="recvTotal">
        </el-pagination>
    </div>
  </el-main>
  <el-main style="height:100%;width:50%;" >
    <div class="conic" style="height:81vh" >
        <el-divider content-position="left">发件箱</el-divider>
        <div v-for="(msg,index) in sendMsg" :key="index" class="card card-2" @click="clickSendMsg($event, msg)">
          <h3>{{msg.msgTitle}}</h3>
          <p> {{msg.msgPre}}</p>
        </div>
        <el-pagination
          ref="sendPage"
          background
          layout="prev, pager, next"
          @current-change="sendCurrentChange"
          :page-size="pageSize"
          :total="sendTotal">
        </el-pagination>
    </div>
  </el-main>
<el-dialog :title="dialogData.title" :visible.sync="dialogTableVisible">
  <div class="demo-image__preview">
    <el-image 
      v-for="(imgsrc,index) in dialogImgSrcList" :key="index"
      style= "width: 100px; height: 100px"
      :src="imgsrc"
      :preview-src-list="dialogImgSrcList">
    </el-image>
    <p>
      类型：{{dialogData.type}}
    </p>
    <p>
      描述：{{dialogData.content}}
    </p>
    <el-button-group v-if="msgShowBnt">
      <el-button type="warning" @click="reject" plain  icon="el-icon-check" >拒绝</el-button>
      <el-button type="success" @click="accept" plain  icon="el-icon-check" >接受</el-button>
    </el-button-group>
  </div>
</el-dialog>

<el-dialog :title="dialogData.title" :visible.sync="dialogSendVisible">
<div class="demo-image__preview">
  <el-image 
    v-for="(imgsrc,index) in dialogImgSrcList" :key="index"
    style= "width: 100px; height: 100px"
    :src="imgsrc"
    :preview-src-list="dialogImgSrcList">
  </el-image>
  <p>
    类型：{{dialogData.type}}
  </p>
  <p>
    描述：{{dialogData.content}}
  </p>
  <p>
    当前状态：{{dialogData.msgData.msg_status}}
  </p>
</div>
</el-dialog>
</el-container>
</div>
</template>

<script>
// axios的引入
import axios from "axios";
axios.defaults.withCredentials=true;

export default {
  data(){
    return{
      recvMsg:[{msgTitle:'', msgPre:'', msgData:{}},],
      sendMsg:[{msgTitle:'', msgPre:'', msgData:{}},],
      recvTotal:null,
      sendTotal:null,
      pageSize:4,
      //对话框相关
      dialogTableVisible:false,
      dialogSendVisible:false,
      dialogData:{title:'', type:'', content:'', msgData:{'msg_status':''}},
      dialogImgSrcList:[],
    }
  },
  computed:{
    msgShowBnt(){
      if(this.dialogData.msgData == null)
        return 0;
      if(this.dialogData.msgData.msg_status == 'undo'){
        return 1;
      }else{
        return 0;
      }
    }
  },
  mounted(){
    //this.getMsg();
  },
  activated(){
    this.getMsg();
  },
  methods:{
    getMsg(){
      let param = {'page_index':1, 'page_size':this.pageSize};
      axios.post(this.$store.state.host + '/message/recv_page', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/recv_page 接口调用成功', response.data);
            this.recvMsg.splice(0);
            this.recvTotal = response.data.total
            let msgList = response.data.data;
            for(let i = 0, len = msgList.length; i < len; ++i){
              this.recvMsg.push({ 'msgTitle':msgList[i].msg_type, 
                                  'msgPre':msgList[i].msg_time + "  来自用户 " + msgList[i].msg_from,
                                  'msgData':msgList[i]});
            }
            this.$message({'message':'收件箱读取成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/recv_page 接口调用失败', error.response);
          this.$message('获取收件箱信息失败');
        }
      )
      axios.post(this.$store.state.host + '/message/send_page', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/send_page 接口调用成功', response.data);
            this.sendMsg.splice(0);
            this.sendTotal = response.data.total
            let msgList = response.data.data;
            for(let i = 0, len = msgList.length; i < len; ++i){
              this.sendMsg.push({ 'msgTitle':msgList[i].msg_type, 
                                  'msgPre':msgList[i].msg_time + "  发送至用户 " + msgList[i].msg_to,
                                  'msgData':msgList[i]});
            }
            this.$message({'message':'发件箱读取成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/send_page 接口调用失败', error.response);
          this.$message('获取发件箱信息失败');
        }
      )
    },
    clickMsg(event, msg){
      msg = msg.msgData;
      console.log('clickMsg:', event, msg);
      //准备数据
      this.dialogData.title = "来自用户：" + msg.msg_from;
      this.dialogData.type = msg.msg_type;
      this.dialogData.content = msg.msg_txt;
      this.dialogData.msgData = msg;
      this.dialogImgSrcList.splice(0);
      //请求图片
      let param = {'msg_id':msg.msg_id};
      axios.post(this.$store.state.host + '/images/get_msgimgs', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/images/get_msgimgs 接口请求成功', response.data);
            for(let i = 0, len = response.data.images_id.length; i < len; ++i){
              this.dialogImgSrcList.push(this.$store.state.host + '/images/msgimg/' 
                                          + response.data.images_id[i].toString());
            }
          }
        },
        error => {
          console.log('/images/get_msgimgs 接口请求失败', error.response);
          this.$message('信息图片获取失败');
        }
      )
      //弹出对话框
      this.dialogTableVisible=true;
    },
    clickSendMsg(event, msg){
      msg = msg.msgData;
      this.dialogData.title = "发送至用户：" + msg.msg_to;
      this.dialogData.type = msg.msg_type;
      this.dialogData.content = msg.msg_txt;
      this.dialogData.msgData = msg;
      this.dialogImgSrcList.splice(0);
      //请求图片
      let param = {'msg_id':msg.msg_id};
      axios.post(this.$store.state.host + '/images/get_msgimgs', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/images/get_msgimgs 接口请求成功', response.data);
            for(let i = 0, len = response.data.images_id.length; i < len; ++i){
              this.dialogImgSrcList.push(this.$store.state.host + '/images/msgimg/' 
                                          + response.data.images_id[i].toString());
            }
          }
        },
        error => {
          console.log('/images/get_msgimgs 接口请求失败', error.response);
          this.$message('信息图片获取失败');
        }
      )
      //弹出对话框
      this.dialogSendVisible=true;
    },
    recvCurrentChange(val){
      console.log('recvCurrentChange:', val);
      this.recvMsg.splice(0);
      let param = {'page_index':val, 'page_size':this.pageSize};
      axios.post(this.$store.state.host+'/message/recv_page', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/recv_page 接口请求成功', response.data);
            this.recvTotal = response.data.total;
            let msgList = response.data.data;
            for(let i = 0, len = msgList.length; i < len; ++i){
              this.recvMsg.push({ 'msgTitle':msgList[i].msg_type, 
                                  'msgPre':msgList[i].msg_time + "  来自用户 " + msgList[i].msg_from,
                                  'msgData':msgList[i]});
            }
            this.$message({'message':'收件箱读取成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/recv_page 接口调用失败', error.response);
          this.$message('获取收件箱信息失败');
        }
      )
    },
    sendCurrentChange(val){
      console.log('sendCurrentChange:', val);
      this.sendMsg.splice(0);
      let param = {'page_index':val, 'page_size':this.pageSize};
      axios.post(this.$store.state.host+'/message/send_page', param).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/send_page 接口请求成功', response.data);
            this.sendTotal = response.data.total;
            let msgList = response.data.data;
            for(let i = 0, len = msgList.length; i < len; ++i){
              this.sendMsg.push({ 'msgTitle':msgList[i].msg_type, 
                                  'msgPre':msgList[i].msg_time + "  发送至用户 " + msgList[i].msg_to,
                                  'msgData':msgList[i]});
            }
            this.$message({'message':'发件箱读取成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/send_page 接口调用失败', error.response);
          this.$message('获取发件箱信息失败');
        }
      )
    },
    accept(){
      let msg_id = this.dialogData.msgData.msg_id;
      axios.post(this.$store.state.host + '/message/accept', {'msg_id':msg_id}).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/accept 接口调用成功', response.data);
            for(let i = 0, len = this.recvMsg.length; i < len; ++i){
              if(this.recvMsg[i].msgData.msg_id == msg_id){
                this.recvMsg[i].msgData.msg_status = 'accept';
              }
            }
            for(let i = 0, len = this.sendMsg.length; i < len; ++i){
              if(this.sendMsg[i].msgData.msg_id == msg_id){
                this.sendMsg[i].msgData.msg_status = 'accept';
              }
            }
            this.$message({'message':'消息接受成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/accept 接口调用失败', error.response);
          this.$message('消息接受失败');
        }
      )
    },
    reject(){
      let msg_id = this.dialogData.msgData.msg_id;
      axios.post(this.$store.state.host + '/message/reject', {'msg_id':msg_id}).then(
        response => {
          if(response.data.msg == 'ok'){
            console.log('/message/reject 接口调用成功', response.data);
            for(let i = 0, len = this.recvMsg.length; i < len; ++i){
              if(this.recvMsg[i].msgData.msg_id == msg_id){
                this.recvMsg[i].msgData.msg_status = 'reject';
              }
            }
            for(let i = 0, len = this.sendMsg.length; i < len; ++i){
              if(this.sendMsg[i].msgData.msg_id == msg_id){
                this.sendMsg[i].msgData.msg_status = 'reject';
              }
            }
            this.$message({'message':'消息拒绝成功', 'type':'success'});
          }
        },
        error => {
          console.log('/message/reject 接口调用失败', error.response);
          this.$message('消息拒绝失败');
        }
      )
    }
  }
}
</script>

<style scoped>
body{
  font-family: 'Nunito', sans-serif;
  padding: 50px;
}
.card{
  border-radius: 4px;
  background: rgb(239, 240, 210);
  box-shadow: 0 6px 10px rgba(0,0,0,.08), 0 0 6px rgba(0,0,0,.05);
  transition: .3s transform cubic-bezier(.155,1.105,.295,1.12),.3s box-shadow,.3s -webkit-transform cubic-bezier(.155,1.105,.295,1.12);
  padding: 14px 80px 18px 36px;
  cursor: pointer;
}

.card:hover{
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06);
}

.card h3{
  font-weight: 600;
  font-size:20px;
  margin-top:5px;
  margin-bottom:5px;
}

.card img{
  position: absolute;
  top: 20px;
  right: 30px;
  max-height: 120px;
}

.card-1{
  /* background-image: url(https://ionicframework.com/img/getting-started/ionic-native-card.png); */
  background-image: url("../assets/msg-open-half.png");
  background-repeat: no-repeat;
  background-position: right;
  background-size: 120px;
  background-color:rgb(252, 252, 231);
  width:90%;
  height:19%;
  margin:2%;
}

.card-2{
  /* background-image: url(https://ionicframework.com/img/getting-started/ionic-native-card.png); */
  background-image: url("../assets/msg-open-half.png");
  background-repeat: no-repeat;
  background-position: right;
  background-size: 120px;
  background-color:aliceblue;
  width:90%;
  height:19%;
  margin:2%;
}

@media(max-width: 990px){
  .card{
    margin: 20px;
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

@-webkit-keyframes rotate {
  100% {
    transform: rotate(1turn);
  }
}

@keyframes rotate {
  100% {
    transform: rotate(1turn);
  }
}
.conic {
  position: relative;
  z-index: 0;
  margin: 6px;
  border-radius: 10px;
  overflow: hidden;
  padding: 2rem;
}
.conic::before {
  content: "";
  position: absolute;
  z-index: -2;
  left: -50%;
  top: -50%;
  width: 200%;
  height: 200%;
  background-color: rgb(182, 234, 211);
  background-repeat: no-repeat;
  background-position: 0 0;
  background-image: conic-gradient(transparent, #c5f4ff, transparent 30%);
  -webkit-animation: rotate 4s linear infinite;
          animation: rotate 4s linear infinite;
}
.conic::after {
  content: "";
  position: absolute;
  z-index: -1;
  left: 6px;
  top: 6px;
  width: calc(100% - 12px);
  height: calc(100% - 12px);
  background: #ffffffb1;
  border-radius: 5px;
}

.conic-demo::after {
  -webkit-animation: opacityChange 5s infinite linear;
          animation: opacityChange 5s infinite linear;
}

@-webkit-keyframes opacityChange {
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

@keyframes opacityChange {
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>