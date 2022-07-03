<template>
<div>
  <div id="title">
    <h1>人间花木 / 同济大学嘉定校区植物地图共建系统</h1>
  </div>
<ul>
  <li class="booking-card" style="background-image: url(https://images.unsplash.com/photo-1578944032637-f09897c5233d?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&ixid=eyJhcHBfaWQiOjE0NTg5fQ)">
    <div class="book-container">
      <div class="content">
        <button class="btn" @click="toMapPub" >游客进入</button>
      </div>
    </div>
    <div class="informations-container">
      <h2 class="title">共享植物地图</h2>
      <p class="sub-title">同济大学嘉定校区</p>
      <div class="more-information">
        <div class="info-and-date-container">
          <div class="box date">
            <svg class="icon" style="width:24px;height:24px" viewBox="0 0 24 24">
            <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z" />
            </svg>
            <p>创建于2022-06-22</p>
          </div>
        </div>
        <p class="disclaimer">分享、开源、共建。</p>
        </div>
    </div>
  </li>
  <li class="booking-card" style="background-image: url(https://images.unsplash.com/photo-1580137197581-df2bb346a786?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&ixid=eyJhcHBfaWQiOjE0NTg5fQ);">
    <div class="book-container">
      <div class="content">
        <button class="btn" @click="toMapPri">用户进入</button>
      </div>
    </div>
    <div class="informations-container">
      <h2 class="title">私人植物地图</h2>
      <p class="sub-title">分享的同时记录您的个人足迹</p>
      <div class="more-information">
        <div class="info-and-date-container">
          <div class="box date">
            <svg class="icon" style="width:24px;height:24px" viewBox="0 0 24 24">
            <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z" />
            </svg>
            <p>创建于2022-06-22</p>
          </div>
        </div>
        <p class="disclaimer">最终解释权归本站所有</p>
        </div>
    </div>
  </li>
  <li class="booking-card" style="background-image: url(https://images.unsplash.com/photo-1579489225078-27977a77bf72?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&ixid=eyJhcHBfaWQiOjE0NTg5fQ);">
    <div class="book-container">
      <div class="content">
        <button class="btn" @click="toHub">游客进入</button>
      </div>
    </div>
    <div class="informations-container">
      <h2 class="title">植物仓库</h2>
      <p class="sub-title">探索植物百科的秘密</p>
      <div class="more-information">
        <div class="info-and-date-container">
          <div class="box info">
            <svg class="icon" style="width:24px;height:24px" viewBox="0 0 24 24">
              <path fill="currentColor" d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z" />
            </svg>
            <p>数据来源于网络</p>
          </div>
          <div class="box date">
            <svg class="icon" style="width:24px;height:24px" viewBox="0 0 24 24">
              <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z" />
            </svg>
            <p>更新于2022-06-22</p>
          </div>
        </div>
        <p class="disclaimer">收录中国植物名录3万8千余条，用户可将其中任意植物添加至植物仓库</p>
        </div>
    </div>
  </li>
  <li class="booking-card" style="background-image: url(https://images.unsplash.com/photo-1532509854226-a2d9d8e66f8e?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&ixid=eyJhcHBfaWQiOjE0NTg5fQ);">
    <div class="book-container">
      <div class="content">
        <button class="btn" @click="toMsg">用户进入</button>
      </div>
    </div>
    <div class="informations-container">
      <h2 class="title">植物通讯箱</h2>
      <p class="sub-title">守护每一个植物数据的成长</p>
      
      <div class="more-information">
        <div class="info-and-date-container">
          <div class="box info">
            <svg class="icon" style="width:24px;height:24px" viewBox="0 0 24 24">
              <path fill="currentColor" d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z" />
            </svg>
            <p>登录后使用</p>
          </div>
        </div>
        <p class="disclaimer">植物通讯箱是一个用于用户之间发送与处理关于地图植物点的特定消息的信箱。用户可以在植物通讯箱中处理其他人发送的对地图植物点的维护与更新信息，以提高信息的时效性与准确性。</p>
        </div>
    </div>
  </li>
  


</ul>
</div>
</template>

<script>
export default {
  data(){
    return {
      // imgurls:[require('../assets/head1.jpg'),
      //         require('../assets/head2.jpg'),
      //         require('../assets/head3.jpg'),
      //         require('../assets/head4.jpg')]
    }
  },
  methods:{
    toMapPub(){
      this.$router.push({name:'PageMappub'});
    },
    toMapPri(){
      if(this.$store.state.login){
        this.$router.push({name:'PageMappri'});
      }else{
        this.$router.push({name:'Login'});
      }
    },
    toHub(){
      this.$router.push({name:'PageHub'});
    },
    toMsg(){
      if(this.$store.state.login){
        this.$router.push({name:'PageMessage'});
      }else{
        this.$router.push({name:'Login'});
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  font-family: "Sofia", sans-serif;
}

#title{
  margin-left:60px;
  margin-top:20px;
}

h1 {
  color:rgb(130, 207, 207);
  font-weight: 1000;
}

h2 {
  color: #0a4870;
  font-weight: 500;
}

ul {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0px;
  margin-left: 60px;
  margin-top: 30px;
}
ul .booking-card {
  position: relative;
  width: 85%;
  display: flex;
  flex: 0 0 20%;
  flex-direction: column;
  margin: 20px;
  margin-bottom: 30px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  overflow: hidden;
  background-position: center center;
  background-size: cover;
  text-align: center;
  color: #0a4870;
  transition: 0.3s;
}
ul .booking-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 72, 112, 0);
  transition: 0.3s;
}
ul .booking-card .book-container {
  height: 200px;
}
ul .booking-card .book-container .content {
  position: relative;
  opacity: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  transform: translateY(-200px);
  transition: 0.3s;
}
ul .booking-card .book-container .content .btn {
  border: 3px solid white;
  padding: 10px 15px;
  background: none;
  text-transform: uppercase;
  font-weight: bold;
  font-size: 1.3em;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}
ul .booking-card .book-container .content .btn:hover {
  background: white;
  border: 0px solid white;
  color: #0a4870;
}
ul .booking-card .informations-container {
  flex: 1 0 auto;
  padding: 20px;
  background: #f0f0f0;
  transform: translateY(206px);
  transition: 0.3s;
}
ul .booking-card .informations-container .title {
  position: relative;
  padding-bottom: 10px;
  margin-bottom: 10px;
  font-weight: bold;
  font-size: 1.2em;
}
ul .booking-card .informations-container .title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  width: 50px;
  margin: auto;
  background: #0a4870;
}
ul .booking-card .informations-container .price {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}
ul .booking-card .informations-container .price .icon {
  margin-right: 10px;
}
ul .booking-card .informations-container .more-information {
  opacity: 0;
  transition: 0.3s;
}
ul .booking-card .informations-container .more-information .info-and-date-container {
  display: flex;
}
ul .booking-card .informations-container .more-information .info-and-date-container .box {
  flex: 1 0;
  padding: 15px;
  margin-top: 20px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  background: white;
  font-weight: bold;
  font-size: 0.9em;
}
ul .booking-card .informations-container .more-information .info-and-date-container .box .icon {
  margin-bottom: 5px;
}
ul .booking-card .informations-container .more-information .info-and-date-container .box.info {
  color: #ec992c;
  margin-right: 10px;
}
ul .booking-card .informations-container .more-information .disclaimer {
  margin-top: 20px;
  font-size: 0.8em;
  color: #7d7d7d;
}
ul .booking-card:hover::before {
  background: rgba(10, 72, 112, 0.6);
}
ul .booking-card:hover .book-container .content {
  opacity: 1;
  transform: translateY(0px);
}
ul .booking-card:hover .informations-container {
  transform: translateY(0px);
}
ul .booking-card:hover .informations-container .more-information {
  opacity: 1;
}

@media (max-width: 768px) {
  ul .booking-card::before {
    background: rgba(10, 72, 112, 0.6);
  }
  ul .booking-card .book-container .content {
    opacity: 1;
    transform: translateY(0px);
  }
  ul .booking-card .informations-container {
    transform: translateY(0px);
  }
  ul .booking-card .informations-container .more-information {
    opacity: 1;
  }
}
.credits {
  display: table;
  background: #0a4870;
  color: white;
  line-height: 25px;
  margin: 10px auto;
  padding: 20px;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  text-align: center;
}
.credits a {
  color: #e3ebf1;
}

h1 {
  margin: 10px 20px;
}
</style>