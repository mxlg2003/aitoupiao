<template>
  <BasicLayout>
    <template #wrapper>
      <el-row :gutter="10">
        <el-col :span="6" :xs="24">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>个人信息</span>
            </div>
            <div>
              <div class="text-center">
                <!--                上传头像-->
                <!--                <userAvatar :user="user" />-->
              </div>
              <ul class="list-group">
                <li class="list-group-item">
                  <svg-icon icon-class="number" />登录名
                  <div class="pull-right">{{ user.login_name }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="user" />用户名称
                  <div class="pull-right">{{ user.user_name }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="date" />生日
                  <div class="pull-right">{{ user.birthday }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="phone" />手机号码
                  <div class="pull-right">{{ user.phone }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="wechat" />微信号
                  <div class="pull-right">{{ user.wechat_no }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="email" />邮箱
                  <div class="pull-right">{{ user.email }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="tree" />所属部门
                  <div class="pull-right">{{ user.department_name }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="peoples" />所属角色
                  <div class="pull-right">{{ user.role_name }}</div>
                </li>
                <li class="list-group-item">
                  <svg-icon icon-class="time" />注册时间
                  <div class="pull-right">{{ parseTime(user.create_time) }}</div>
                </li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="18" :xs="24">
          <el-card>
            <div slot="header" class="clearfix">
              <span>基本资料</span>
            </div>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="基本资料" name="userinfo">
                <userInfo :user="user" />
              </el-tab-pane>
              <el-tab-pane label="修改密码" name="resetPwd">
                <resetPwd :user="user" />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </BasicLayout>
</template>

<script>
import userInfo from './userInfo'
import resetPwd from './resetPwd'
import { getUser } from '@/api/system/sysuser'
import { getUserInfo } from '@/api/login'

export default {
  name: 'Profile',
  components: {
    // userAvatar,
    userInfo,
    resetPwd
  },
  data() {
    return {
      user: {},
      activeTab: 'userinfo'
    }
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    getUserInfo() {
      getUserInfo().then(res => {
        getUser({ user_id: res.user.id }).then(response => {
          this.user = response.data
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .list-group-item{
    padding: 18px 0;
  }
  .svg-icon{
    margin-right: 5px;
  }
</style>
