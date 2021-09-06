<template>
  <BasicLayout>
    <template #wrapper>
      <el-card class="box-card">
        <el-row :gutter="20">
          <!--部门数据-->
          <el-col :span="4" :xs="24">
            <div class="head-container">
              <el-input
                v-model="dept_name"
                placeholder="请输入部门名称"
                clearable
                size="small"
                prefix-icon="el-icon-search"
                style="margin-bottom: 20px"
              />
            </div>
            <div class="head-container">
              <el-tree
                ref="tree"
                :data="deptOptions"
                :props="defaultProps"
                :expand-on-click-node="false"
                :filter-node-method="filterNode"
                default-expand-all
                @node-click="handleNodeClick"
              />
            </div>
          </el-col>
          <!--用户数据-->
          <el-col :span="20" :xs="24">
            <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
              <el-form-item>
                <el-input
                  v-model="queryParams.user_name"
                  placeholder="请输入用户名称"
                  clearable
                  size="small"
                  style="width: 240px"
                  @keyup.enter.native="handleQuery"
                />
              </el-form-item>
              <el-form-item>
                <el-input
                  v-model="queryParams.phone"
                  placeholder="请输入手机号码"
                  clearable
                  size="small"
                  style="width: 240px"
                  @keyup.enter.native="handleQuery"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
                <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
              </el-form-item>
            </el-form>

            <el-row :gutter="10" class="mb8">
              <el-col :span="1.5">
                <el-button
                  v-permisaction="['system:sysuser:add']"
                  type="primary"
                  icon="el-icon-plus"
                  size="mini"
                  @click="handleAdd"
                >新增</el-button>
              </el-col>
            </el-row>
            <el-table
              v-loading="loading"
              :data="userList"
            >
              <el-table-column type="selection" width="45" align="center" />
              <el-table-column label="登录名" align="center" prop="login_name" :show-overflow-tooltip="true" />
              <el-table-column label="用户名" align="center" prop="user_name" :show-overflow-tooltip="true" />
              <el-table-column label="所属部门" align="center" prop="department_name" :show-overflow-tooltip="true" />
              <el-table-column label="所属角色" align="center" prop="role_name" :show-overflow-tooltip="true" />
              <el-table-column label="手机号码" align="center" prop="phone" width="120" />
              <el-table-column label="微信号码" align="center" prop="wechat_no" width="120" />
              <el-table-column label="邮箱" align="center" prop="email" width="120" />
              <el-table-column label="生日" align="center" width="120">
                <template slot-scope="scope">
                  <span>{{ scope.row.birthday }}</span>
                </template>
              </el-table-column>
              <el-table-column label="性别" align="center" width="50">
                <template slot-scope="scope">
                  <span v-if="scope.row.gender === 1">男</span>
                  <span v-else-if="scope.row.gender === 2">女</span>
                  <span v-else>未知</span>
                </template>
              </el-table-column>

              <el-table-column label="注册时间" align="center" prop="create_time" width="165">
                <template slot-scope="scope">
                  <span>{{ parseTime(scope.row.create_time) }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                align="center"
                width="180"
                class-name="small-padding fixed-width"
              >
                <template slot-scope="scope">
                  <el-button
                    v-permisaction="['system:sysuser:edit']"
                    size="mini"
                    type="text"
                    icon="el-icon-edit"
                    @click="handleUpdate(scope.row)"
                  >修改</el-button>
                  <el-button
                    v-if="scope.row.userId !== 1"
                    v-permisaction="['system:sysuser:remove']"
                    size="mini"
                    type="text"
                    icon="el-icon-delete"
                    @click="handleDelete(scope.row)"
                  >删除</el-button>
                  <el-button
                    v-permisaction="['system:sysuser:resetPassword']"
                    size="mini"
                    type="text"
                    icon="el-icon-key"
                    @click="handleResetPwd(scope.row)"
                  >重置</el-button>
                </template>
              </el-table-column>
            </el-table>

            <pagination
              v-show="total>0"
              :total="total"
              :page.sync="queryParams.page"
              :limit.sync="queryParams.pageSize"
              @pagination="getList"
            />
          </el-col>
        </el-row>
      </el-card>
      <!-- 添加或修改参数配置对话框 -->
      <el-dialog :title="title" :visible.sync="open" width="700px">
        <el-form ref="form" :model="form" :rules="rules" label-width="80px">
          <el-row>
            <el-col v-if="!form.id" :span="12">
              <el-form-item label="登录名" prop="login_name">
                <el-input v-model="form.login_name" placeholder="请输入登录名" @blur="checkLoginName" />
              </el-form-item>
            </el-col>
            <el-col v-if="!form.id" :span="12">
              <el-form-item label="密码" prop="password">
                <el-input v-model="form.password" placeholder="请输入密码" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="用户名称" prop="user_name">
                <el-input v-model="form.user_name" placeholder="请输入用户名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="手机号码" prop="phone">
                <el-input v-model="form.phone" placeholder="请输入手机号码" maxlength="11" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="微信号" prop="wechat_no">
                <el-input v-model="form.wechat_no" placeholder="请输入邮箱" maxlength="50" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" placeholder="请输入邮箱" maxlength="50" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="所属角色" prop="role_id">
                <el-select v-model="form.role_id" placeholder="请选择" @change="$forceUpdate()">
                  <el-option
                    v-for="item in roleOptions"
                    :key="item.id"
                    :label="item.role_name"
                    :value="item.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="归属部门" prop="department_id">
                <TreeSelect
                  v-model="form.department_id"
                  :options="deptOptions"
                  :normalizer="normalizer"
                  placeholder="请选择归属部门"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="生日" prop="birthday">
                <el-date-picker v-model="form.birthday" class="date" type="date" value-format="yyyy-MM-dd" placeholder="请选择生日" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="用户性别">
                <el-select v-model="form.gender" placeholder="请选择">
                  <el-option label="未知" value="0" />
                  <el-option label="男" value="1" />
                  <el-option label="女" value="2" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="备注">
                <el-input v-model="form.remarks" type="textarea" placeholder="请输入内容" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </el-dialog>
    </template>
  </BasicLayout>
</template>

<script>
import { userList, getUser, delUser, saveUser, checkLoginName, resetUserPwd } from '@/api/system/sysuser'
import { getDeptList } from '@/api/system/dept'
import { getRoleList } from '@/api/system/role'
import TreeSelect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

export default {
  name: 'User',
  components: { TreeSelect },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 总条数
      total: 0,
      check_login_name: true,
      // 用户表格数据
      userList: null,
      // 弹出层标题
      title: '',
      // 部门树选项
      deptOptions: undefined,
      // 是否显示弹出层
      open: false,
      // 部门名称
      dept_name: undefined,
      // 角色选项
      roleOptions: [],
      // 表单参数
      form: {},
      defaultProps: {
        children: 'children',
        label: 'department_name'
      },
      // 查询参数
      queryParams: {
        page: 1,
        pageSize: 10,
        user_name: undefined,
        phone: undefined,
        dept_id: undefined
      },
      // 表单校验
      rules: {
        user_name: [
          { required: true, message: '用户名称不能为空', trigger: 'blur' }
        ],
        department_id: [
          { required: true, message: '归属部门不能为空', trigger: 'blur' }
        ],
        role_id: [
          { required: true, message: '所属角色不能为空', trigger: 'blur' }
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
  watch: {
    // 根据名称筛选部门树
    dept_name(val) {
      this.$refs.tree.filter(val)
    }
  },
  created() {
    this.getList()
    this.getTreeSelect()
    this.getRoleTree()
  },
  methods: {
    /** 查询用户列表 */
    getList() {
      this.loading = true
      userList(this.queryParams).then(response => {
        this.userList = response.data.user_list
        this.total = response.data.total
        this.loading = false
      }
      )
    },
    // 获取部门信息
    getTreeSelect() {
      getDeptList().then(response => {
        this.deptOptions = response.data
      })
    },
    // 获取角色信息
    getRoleTree() {
      getRoleList({ page: 1, pageSize: 999 }).then(response => {
        this.roleOptions = response.data
      })
    },
    // 筛选节点
    filterNode(value, data) {
      if (!value) return true
      return data.department_name.indexOf(value) !== -1
    },
    // 节点单击事件
    handleNodeClick(data) {
      this.queryParams.dept_id = data.id
      this.getList()
    },
    // 验证登录名是否可注册
    checkLoginName() {
      checkLoginName({ login_name: this.form.login_name }).then(response => {
        if (response.data > 0) {
          this.check_login_name = true
          this.msgError('该用户名已存在！')
        } else {
          this.check_login_name = false
        }
      })
    },
    /** 转换菜单数据结构 */
    normalizer(node) {
      if (node.children && !node.children.length) {
        delete node.children
      }
      return {
        id: node.id,
        label: node.department_name,
        children: node.children
      }
    },
    // 取消按钮
    cancel() {
      this.open = false
      this.reset()
    },
    // 表单重置
    reset() {
      this.form = {
        id: undefined,
        login_name: undefined,
        password: undefined,
        department_id: undefined,
        role_id: undefined,
        user_name: undefined,
        phone: undefined,
        email: undefined,
        wechat_no: undefined,
        gender: 0,
        remark: undefined
      }
      this.resetForm('form')
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.page = 1
      this.getList()
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = []
      this.resetForm('queryForm')
      this.handleQuery()
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset()
      this.open = true
      this.title = '添加用户'
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      getUser({ user_id: row.id }).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改用户'
      })
    },
    /** 重置密码按钮操作 */
    handleResetPwd(row) {
      this.$prompt('请输入"' + row.user_name + '"的新密码', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        resetUserPwd({ user_id: row.id, password: value }).then(response => {
          if (response.code === 200) {
            this.msgSuccess(response.message)
          }
        })
      }).catch(() => {})
    },
    /** 提交按钮 */
    submitForm: function() {
      if (!this.form.id) {
        this.checkLoginName()
        if (this.check_login_name) {
          this.msgError('该用户名已存在！')
          return
        }
        if (this.form.login_name === undefined || this.form.login_name === '') {
          this.msgSuccess.msgError('登录名必填')
          return
        }
        if (this.form.password === undefined || this.form.password === '') {
          this.msgSuccess.msgError('密码必填')
          return
        }
      }
      this.$refs['form'].validate(valid => {
        if (valid) {
          saveUser(this.form).then(response => {
            if (response.code === 200) {
              this.msgSuccess(response.message)
              this.open = false
              this.getList()
            }
          })
        }
      })
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      this.$confirm('是否确认删除用户"' + row.user_name + '"?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return delUser({ user_id: row.id })
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功，为不影响他人浏览，此操作将做不入库处理')
      }).catch(function() {})
    }
  }
}
</script>
