<template>
  <BasicLayout>
    <template #wrapper>
      <el-card class="box-card">
        <el-form ref="queryForm" :model="queryParams" :inline="true">
          <el-form-item>
            <el-input
              v-model="queryParams.role_name"
              placeholder="请输入角色名称"
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
              v-permisaction="['system:sysrole:add']"
              type="primary"
              icon="el-icon-plus"
              size="mini"
              @click="handleAdd"
            >新增</el-button>
          </el-col>
        </el-row>

        <el-table v-loading="loading" :data="roleList">
          <el-table-column label="角色名称" prop="role_name" :show-overflow-tooltip="true" width="150" />
          <el-table-column label="权限字符" prop="roleKey" :show-overflow-tooltip="true" width="150" />
          <el-table-column label="显示顺序" prop="idx" width="100" />
          <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button
                v-permisaction="['system:sysrole:edit']"
                size="mini"
                type="text"
                icon="el-icon-edit"
                @click="handleUpdate(scope.row)"
              >修改</el-button>
              <el-button
                v-permisaction="['system:sysrole:remove']"
                size="mini"
                type="text"
                icon="el-icon-delete"
                @click="handleDelete(scope.row)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <pagination
          v-show="total>0"
          :total="total"
          :page.sync="queryParams.pageIndex"
          :limit.sync="queryParams.pageSize"
          @pagination="getList"
        />

        <!-- 添加或修改角色配置对话框 -->
        <el-dialog :title="title" :visible.sync="open" width="500px">
          <el-form ref="form" :model="form" :rules="rules" label-width="80px">
            <el-form-item label="角色名称" prop="role_name">
              <el-input v-model="form.role_name" placeholder="请输入角色名称" :disabled="isEdit" />
            </el-form-item>
            <el-form-item label="角色顺序" prop="idx">
              <el-input-number v-model="form.idx" controls-position="right" :min="0" />
            </el-form-item>
            <el-form-item label="数据权限" prop="data_permission_type">
              <el-select size='small' v-model="form.data_permission_type" clearable placeholder="请选择" @change="changeDataType"
                         style="width: 40%;margin-bottom:10px;">
                <el-option
                  v-for="item in dataPer"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <div v-if="form.data_permission_type == 4">
                <el-tree
                  :data="deptList"
                  show-checkbox
                  :expand-on-click-node="false"
                  ref="dept"
                  node-key="id"
                  highlight-current
                  :props="defaultDept"
                  :default-checked-keys="defaultDeptList"
                ></el-tree>
              </div>
            </el-form-item>
            <el-form-item label="菜单权限">
              <el-tree
                :data="menuList"
                show-checkbox
                :expand-on-click-node="false"
                ref="menu"
                node-key="id"
                highlight-current
                :props="defaultMenu"
                :default-checked-keys="defaultRoleMenu"
              ></el-tree>
            </el-form-item>
            <el-form-item label="备注">
              <el-input v-model="form.remarks" type="textarea" placeholder="请输入内容" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="submitForm">确 定</el-button>
            <el-button @click="cancel">取 消</el-button>
          </div>
        </el-dialog>
      </el-card>
    </template>
  </BasicLayout>
</template>

<script>
import { getRoleList, getRole, delRole, saveRole } from '@/api/system/role'
import { getMenuList } from '@/api/system/menu'
import { getDeptList } from '@/api/system/dept'

export default {
  name: 'Role',
  components: {

  },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 总条数
      total: 0,
      // 角色表格数据
      roleList: [],
      // 操作权限
      menuList: [],
      defaultMenu: {
        children: 'children',
        label: 'menu_name',
        value: 'id',
        checked: 'selected'
      },
      defaultRoleMenu: [],
      // 数据权限
      deptList: [],
      defaultDept: {
        children: 'children',
        label: 'department_name',
        value: 'id',
        checked: 'selected'
      },
      defaultDeptList: [],
      dataPer: [
        {value: 0, label: '仅自己参与过的数据'},
        {value: 1, label: '本部门数据'},
        {value: 2, label: '本部门及所有子部门数据'},
        {value: 3, label: '全部数据'},
        {value: 4, label: '自定义数据'}
      ],

      // 弹出层标题
      title: '',
      // 是否显示弹出层
      open: false,
      isEdit: false,
      // 查询参数
      queryParams: {
        page: 1,
        pageSize: 10,
        role_name: undefined
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        role_name: [
          { required: true, message: '角色名称不能为空', trigger: 'blur' }
        ],
        data_permission_type: [
          { required: true, message: '数据权限不能为空', trigger: 'blur' }
        ],
        idx: [
          { required: true, message: '角色顺序不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    /** 查询角色列表 */
    getList() {
      this.loading = true
      getRoleList(this.queryParams).then(
        response => {
          this.roleList = response.data
          this.total = response.total
          this.loading = false
        }
      )
    },
    // 修改
    handleUpdate(row) {
      this.reset()
      this.getMenuTreeSelect()
      getRole({ role_id: row.id }).then(response => {
        this.form = response.data.role_info
        this.open = true
        this.title = '修改角色'
        this.isEdit = true
        this.defaultRoleMenu = response.data.role_menu_ids
        this.findAllChildren(this.menuList, this.defaultRoleMenu)
        this.defaultDeptList = response.data.data_permission_ids
        this.findAllChildren(this.deptList, this.defaultDeptList)
        if (this.form.data_permission_type == 4){
          this.getDataDeptList()
        }
      })
    },

    // 获取菜单列表
    getMenuTreeSelect() {
      getMenuList().then(response => {
        this.menuList = response.data
      })
    },

    // 选择数据权限
    changeDataType(e) {
      if (e === 4) {
        this.getDataDeptList();
      } else {
        this.deptList = []
      }
    },

    // 当自定义数据权限时，获取部门列表
    getDataDeptList() {
      getDeptList({}).then(res => {
        if (res.code === 200) {
          this.deptList = res.data;
        } else {
          this.$message({type: 'error', message: res.message})
        }
      })
    },

    // 遍历找出所有子节点
    findAllChildren(data, arr, list) {
      if (data != undefined) {
        data.forEach((item, index) => {
          if (item.children) {
            if (item.children.length !== 0) {
              this.findAllChildren(item.children, arr, list)
            }
          }
          if (item.permissionId) {
            if (item.selected == true) {
              arr.push(item.permissionId);
              list.push(item)
            }
          } else {
            if (item.selected == true) {
              arr.push(item.id)
            }
          }
        })
      }
    },

    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.page = 1
      this.getList()
    },
    // 重置按钮
    resetQuery() {
      this.resetForm('queryForm')
      this.handleQuery()
    },
    // 新增
    handleAdd() {
      this.reset()
      this.getMenuTreeSelect()
      this.open = true
      this.title = '添加角色'
      this.isEdit = false
    },
    // 保存
    submitForm: function() {
      this.form.menu_id_list = this.$refs.menu.getCheckedKeys()
      if (this.form.data_permission_type !== 4) {
        this.form.dept_id_list = []
      } else {
        this.form.dept_id_list = this.$refs.dept.getCheckedKeys()
      }
      this.$refs['form'].validate(valid => {
        saveRole(this.form).then(response => {
          if (response.code === 200) {
            this.msgSuccess(response.message)
            this.open = false
            this.getList()
          }
        })
      })
    },
    // 删除
    handleDelete(row) {
      this.$confirm('是否确认删除"' + row.role_name + '"角色数据?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return delRole({role_id : row.id})
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功，为不影响他人浏览，此操作将做不入库处理')
      }).catch(function() {})
    },
    // 取消按钮
    cancel() {
      this.open = false
      this.reset()
    },
    // 表单重置
    reset() {
      if (this.$refs.menu !== undefined) {
        this.$refs.menu.setCheckedKeys([])
      }
      this.form = {
        id: undefined,
        role_name: undefined,
        idx: 0,
        dept_id_list: [],
        menu_id_list: [],
        remarks: undefined
      }
      this.resetForm('form')
    },
  }
}
</script>
