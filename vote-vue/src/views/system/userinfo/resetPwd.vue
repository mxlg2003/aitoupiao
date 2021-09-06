<template>
  <el-form ref="form" :model="user" :rules="rules" label-width="80px">
    <el-form-item label="旧密码" prop="old_pwd">
      <el-input v-model="user.old_pwd" placeholder="请输入旧密码" type="password" />
    </el-form-item>
    <el-form-item label="新密码" prop="password">
      <el-input v-model="user.password" placeholder="请输入新密码" type="password" />
    </el-form-item>
    <el-form-item label="确认密码" prop="confirmPassword">
      <el-input v-model="user.confirmPassword" placeholder="请确认密码" type="password" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" size="mini" @click="submit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { resetUserPwd } from '@/api/system/sysuser'

export default {
  props: {
    user: { type: Object }
  },
  data() {
    const equalToPassword = (rule, value, callback) => {
      if (this.user.password !== value) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      test: '1test',
      // 表单校验
      rules: {
        old_pwd: [
          { required: true, message: '旧密码不能为空', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '新密码不能为空', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 4 到 20 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '确认密码不能为空', trigger: 'blur' },
          { required: true, validator: equalToPassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submit() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          resetUserPwd({ user_id: this.user.id, old_pwd: this.user.old_pwd, password: this.user.password }).then(res => {
            if (res.code === 200) {
              this.msgSuccess(res.message)
            }
          }
          )
        }
      })
    }
  }
}
</script>
