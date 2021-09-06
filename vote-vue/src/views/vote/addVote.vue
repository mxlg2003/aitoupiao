<template>
  <div class="content">
    <div class="contentLeft">
      <div style="padding-top: 20px; width: 100%; text-align: center; color: #E65D6E; font-weight: 500;">此模型为活动效果示例，仅供参考！</div>
      <div class="phoneFrame">
        <img src="../../assets/iphone1.png" style="width: 100%; height: 100%;">
        <div class="phoneContent">
          <div class="voteTitle">投票活动</div>
          <div class="voteContent" :style="{backgroundImage: 'url(' + imgUrl + ')', backgroundRepeat: 'no-repeat', webkitBackgroundSize: '100% 100%'}">
            <div v-if="voteContentActive === 0">
              <img class="voteBanner" src="@/assets/vote/1598334735.jpg">
              <div class="voteStatistics">
                <div class="statisticsItem">
                  <span>投票项</span><br />
                  <span>10</span>
                </div>
                <div class="statisticsItem">
                  <span>总投票数</span><br />
                  <span>100</span>
                </div>
                <div class="statisticsItem">
                  <span>总访问数</span><br />
                  <span>450</span>
                </div>
              </div>
              <div class="voteSearch">
                <el-input size="mini" placeholder="请输入编号或名称" style="background: #FBF0DA; width: 70%;">
                  <el-button slot="append" icon="el-icon-search"></el-button>
                </el-input>
              </div>
              <div class="voteContentItem">
                <div class="gongGeShow" v-for="item in 20">
                  <div class="gongGeShowItemImg"><img src="@/assets/vote/1.png"></div>
                  <div class="gongGeShowItemContentName">
                    {{ item }}号选手
                  </div>
                  <div class="gongGeShowItemContentTicket">{{ (20 - item) * 5 + 1}} 票</div>
                  <div class="gongGeShowItemButton">
                    <el-button size="mini" style="width: 70px;">投票</el-button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="voteContentActive === 1">
              <div class="explainBox">
                <div class="explainBoxHead">排&nbsp;&nbsp;行&nbsp;&nbsp;榜</div>
                <ul class="explainBoxUl">
                  <li class="explainBoxLi" v-for="(item, index) in 20">
                    <div class="explainBoxIndex" v-if="index === 0" style="font-size: 16px; color: #FC0404; font-weight: 700;">{{item}}</div>
                    <div class="explainBoxIndex" v-else-if="index === 1" style="font-size: 16px; color: #FC5858; font-weight: 600;">{{item}}</div>
                    <div class="explainBoxIndex" v-else-if="index === 2" style="font-size: 16px; color: #FD8181; font-weight: 500;">{{item}}</div>
                    <div class="explainBoxIndex" v-else>{{item}}</div>
                    <div class="explainBoxLiImg">
                      <img src="@/assets/vote/1604280725631.jpg" v-if="item % 3 === 0 ">
                      <img src="@/assets/vote/1.png" v-else-if="item % 3 === 1">
                      <img src="@/assets/vote/160428084213508.jpg" v-else>
                    </div>
                    <div class="explainBoxLiName">
                      {{item}}号选手
                    </div>
                    <div class="explainBoxLiNameTicket">
                      {{ (20 - item) * 5 + 1}} 票
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            <div v-if="voteContentActive === 2">
              <div class="explainBox">
                <div class="explainBoxHead">活&nbsp;&nbsp;动&nbsp;&nbsp;详&nbsp;&nbsp;情</div>
                <div class="activeLine">—— 活动时间 ——</div>
                <div class="activeExplain" style="font-size: 13px;"> 2021-02-01 10:00:00 — 2021-02-07 10:00:00 </div>
                <div class="activeLine">—— 活动规则 ——</div>
                <div class="activeExplain">
                  1.每人每天投票次数：100 <br/>
                  2.每人投票总次数：无限制 <br/>
                  3.每日重复投票给同一选项：允许 <br/>
                </div>
                <div class="activeLine">—— 活动说明 ——</div>
                <div class="activeExplain">
                  为确保活动公平公正，大家一起遵守投票规则哟
                  禁止刷票，否则可能被取消资格
                </div>
                <div class="activeLine">—— 活动主办方 ——</div>
                <div class="activeExplain">
                  请填写有关主办方的信息，该信息将曝光在活动详情页，增加主办方的活动知名度！
                </div>
              </div>
            </div>
          </div>
          <div class="voteFooter">
            <ul>
              <li v-for="(item, index) in voteActiveList" v-bind:class="{bottomActive:index === voteContentActive }" @click="voteActiveClick(index)">{{item}}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="contentRight">
      <ul class="rightUl">
        <li class="rightUlLi" v-for="(item, index) in tabList" v-bind:class="{active:index === activeNum}" @click="handleClick(index)">{{item}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name: "addVote",
    data(){
      return{
        tabList: ['基本设置', '投票设置', '高级设置'],
        voteActiveList: ['首页', '投票排名', '活动详情'],
        activeNum: 0,
        voteContentActive: 0,
        imgUrl: require('@/assets/vote/爱国红.jpg')
      }
    },
    mounted() {},
    methods: {
      handleClick(index) {
        this.activeNum = index
      },
      voteActiveClick(index) {
        this.voteContentActive = index
      }
    }
  }
</script>

<style scoped>
  .content{
    background: #ffffff;
    overflow: hidden;
    width: 100%;
    height: 100%;
    min-height: 1000px;
    min-width: 850px;
    position: relative;
  }
  .contentLeft{
    position: absolute;
    width: 45%;
    float: left;
    min-width: 380px;
    overflow: auto;
    box-sizing: border-box;
    border-right: 2px solid #E0E6ED;
  }

  .phoneFrame{
    position: relative;
    margin: 30px auto;
    width: 380px;
    height: 790px;
  }
  .phoneContent{
    position: absolute;
    width: 343px;
    height: 600px;
    z-index: 5;
    top: 95px;
    left: 20px;
  }

  .voteTitle{
    width: 100%;
    height: 35px;
    line-height: 30px;
    text-align: center;
    color: #444444;
    font-size: 14px;
  }
  .voteContent{
    width: 100%;
    height: 520px;
    border-right: 1px solid #000000;
    overflow-y: scroll;
  }
  .voteContent::-webkit-scrollbar {
    width: 2px;  /* 滚动条宽度 */
  }
  .voteContent::-webkit-scrollbar-thumb {
    /* 滚动条里面小方块 */
    border-radius: 2px;
    box-shadow: inset 0 0 5px rgba(204,204,204, 0.2);
    background: #535353;
  }
  .voteContent::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    box-shadow: inset 0 0 5px rgba(204,204,204, 0.2);
    border-radius: 10px;
    background: #ededed;
  }

  .voteBanner {
    width: 100%;
  }
  .voteStatistics{
    padding-top: 15px;
    margin-top: -10px;
    width: 100%;
    background: #FFF0CC;
    overflow: hidden;
  }
  .statisticsItem{
    width: 33%;
    float: left;
    text-align: center;
    color: #751A04;
  }
  .statisticsItem span:last-child{
    height: 28px;
    line-height: 28px;
    font-weight: 600;
  }
  .voteSearch{
    width: 100%;
    text-align: center;
    background: #FFF0CC;
    padding-bottom: 10px;
  }

  .voteContentItem{
    width: 100%;
    min-height: 800px;
  }
  .gongGeShow{
    width: 40%;
    float: left;
    font-size: 14px;
    overflow: hidden;
    min-height: 200px;
    margin: 15px;
    background-color: #ffffff;
  }
  .gongGeShowItemImg{
    width: 90%;
    margin: 0 auto;
  }
  .gongGeShowItemImg img{
    margin-top: 10px;
    width: 100%;
    height: 120px;
  }
  .gongGeShowItemContentName {
    width: 100%;
    padding-left: 5px;
    margin-bottom: 5px;
    height: 30px;
    overflow: hidden;
  }
  .gongGeShowItemContentTicket {
    color: #E93475;
    width: 100%;
    text-align: center;
    margin-bottom: 5px;
  }
  .gongGeShowItemButton {
    width: 100%;
    text-align: center;
    margin-bottom: 5px;
  }

  .explainBox{
    width: 90%;
    margin: 20px auto;
    min-height: 450px;
    background: #FFF0CC;
    border-radius: 15px;
  }
  .explainBoxHead{
    width: 100%;
    text-align: center;
    font-size: 18px;
    font-weight: 800;
    color: #751A04;
    padding-top: 10px;
  }
  .explainBoxUl {
    margin: 0 0 30px 0;
    padding: 0;
    list-style: none;
    width: 100%;
  }

  .explainBoxLi {
    width: 100%;
    height: 70px;
    overflow: hidden;
    border-bottom: 2px solid #EEEEEE;
    font-size: 14px;
  }
  .explainBoxLi:last-child{
    border-bottom: none;
    margin-bottom: 20px;
  }

  .explainBoxIndex{
    float: left;
    width: 20px;
    height: 70px;
    line-height:70px;
    text-align: center;
  }

  .explainBoxLiImg{
    float: left;
    width: 70px;
    height: 70px;
    line-height:70px;

  }
  .explainBoxLiImg img{
    width: 50px;
    height: 50px;
    margin: 10px 5px;
    border-radius: 35px;
  }

  .explainBoxLiName{
    float: left;
    min-width: 150px;
    height: 70px;
    line-height:70px;
  }
  .explainBoxLiNameTicket{
    float: right;
    min-width: 50px;
    height: 70px;
    line-height:70px;
    margin-right: 7px;
    color: #F66926;
  }

  .activeLine{
    width: 100%;
    text-align: center;
    color: #005BA6;
    margin: 15px 0 15px 0;
    font-size: 14px;
  }
  .activeExplain{
    width: 100%;
    padding: 0 10px 0 10px;
    font-size: 15px;
    line-height: 22px;
  }

  .voteFooter{
    width: 100%;
    height: 45px;
    background: #FFF0CC;
    border-right: 1px solid #000000;
    color: #751A04;
    font-size: 12px;
  }
  .voteFooter ul{
    margin: 0;
    padding: 0;
    list-style: none;
    width: 100%;
    height: 45px;
  }
  .voteFooter li{
    float:left;
    width: 33%;
    margin: 0;
    padding: 0;
    height: 45px;
    line-height: 45px;
    cursor: pointer;
    text-align: center;
  }
  .contentRight{
    position: absolute;
    left: 45%;
    overflow: auto;
    width: 55%;
  }
  .rightUl{
    margin: 0;
    padding: 0;
    list-style: none;
    width: 100%;
    height: 40px;
  }
  .rightUlLi{
    float:left;
    width: 33%;
    margin: 0;
    padding: 0;
    cursor: pointer;
    text-align: center;
    height: 60px;
    line-height: 60px;
    background: #F8F8F8;
    color: #999999;
    border-right: 1px solid #E0E6ED;
    border-bottom: 1px solid #E0E6ED;
  }
  .rightUlLi:last-child{
    border-right: none;
  }
  .active{
    background: #ffffff;
    border-bottom: none;
    color: #F66926;
  }
  .bottomActive {
    color: #F66926;
    font-size: 14px;
  }
</style>
