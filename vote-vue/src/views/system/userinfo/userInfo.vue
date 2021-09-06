<template>
  <el-form ref="form" :model="user" :rules="rules" label-width="80px">
    <el-form-item label="用户名称" prop="user_name">
      <el-input v-model="user.user_name" />
    </el-form-item>
    <el-form-item label="手机号码" prop="phone">
      <el-input v-model="user.phone" />
    </el-form-item>
    <el-form-item label="微信号" prop="wechat_no">
      <el-input v-model="user.wechat_no" />
    </el-form-item>
    <el-form-item label="生日" prop="birthday">
      <el-date-picker v-model="user.birthday" class="date" type="date" value-format="yyyy-MM-dd" placeholder="请选择生日" />
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="user.email" maxlength="50" />
    </el-form-item>
    <el-form-item label="性别">
      <el-select v-model="user.gender" placeholder="请选择">
        <el-option label="未知" value="0" />
        <el-option label="男" value="1" />
        <el-option label="女" value="2" />
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" size="mini" @click="submit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { saveUser } from '@/api/system/sysuser'

export default {
  props: {
    user: { type: Object }
  },
  data() {
    return {
      // 表单校验
      rules: {
        user_name: [
          { required: true, message: '用户名不能为空', trigger: 'blur' }
        ],
        wechat_no: [
          { required: true, message: '微信号不能为空', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '手机号码不能为空', trigger: 'blur' },
          {
            pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
            message: '请输入正确的手机号码',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    submit() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          saveUser(this.user).then(response => {
            if (response.code === 200) {
              this.msgSuccess(response.message)
            }
          })
        }
      })
    }
  }
}
</script>
