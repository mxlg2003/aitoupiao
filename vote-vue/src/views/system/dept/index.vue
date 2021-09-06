<template>
  <BasicLayout>
    <template #wrapper>
      <el-card class="box-card">
        <el-form :inline="true">
          <el-form-item>
            <el-input
              v-model="queryParams.dept_name"
              placeholder="请输入部门名称"
              clearable
              size="small"
              @keyup.enter.native="handleQuery"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              class="filter-item"
              type="primary"
              icon="el-icon-search"
              size="mini"
              @click="handleQuery"
            >搜索</el-button>
            <el-button
              v-permisaction="'/system/dept/create'"
              class="filter-item"
              type="primary"
              icon="el-icon-plus"
              size="mini"
              @click="handleAdd"
            >新增</el-button>
          </el-form-item>
        </el-form>

        <el-table
          v-loading="loading"
          :data="deptList"
          row-key="id"
          default-expand-all
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
        >
          <el-table-column prop="department_name" label="部门名称" />
          <el-table-column prop="idx" label="排序" width="200" />
          <el-table-column label="创建时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="remarks" label="备注" />
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button
                v-permisaction="'/system/dept/edit'"
                size="mini"
                type="text"
                icon="el-icon-edit"
                @click="handleUpdate(scope.row)"
              >修改</el-button>
              <el-button
                v-permisaction="'/system/dept/create'"
                size="mini"
                type="text"
                icon="el-icon-plus"
                @click="handleAdd(scope.row)"
              >新增</el-button>
              <el-button
                v-permisaction="'/system/dept/delete'"
                size="mini"
                type="text"
                icon="el-icon-delete"
                @click="handleDelete(scope.row)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 添加或修改部门对话框 -->
        <el-dialog :title="title" :visible.sync="open" width="600px">
          <el-form ref="form" :model="form" :rules="rules" label-width="80px">
            <el-row>
              <el-col :span="24">
                <el-form-item label="上级部门" prop="parent_id">
                  <treeselect v-if="!isEdit" v-model="form.parent_id" :options="deptOptions" :normalizer="normalizer" :show-count="true" placeholder="选择上级部门" />
                  <el-input v-else v-model="form.parent_name" placeholder="请输入部门名称" disabled="disabled"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="部门名称" prop="department_name">
                  <el-input v-model="form.department_name" placeholder="请输入部门名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="显示排序" prop="idx">
                  <el-input-number v-model="form.idx" controls-position="right" :min="0" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="备注" prop="remarks">
                  <el-input v-model="form.remarks" placeholder="请输入备注" />
                </el-form-item>
              </el-col>
            </el-row>
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
import { getDeptList, getDept, delDept, saveDept } from '@/api/system/dept'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

export default {
  name: 'Dept',
  components: { Treeselect },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 表格树数据
      deptList: [],
      // 部门树选项
      deptOptions: [],
      // 弹出层标题
      title: '',
      isEdit: false,
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        dept_name: undefined,
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        parent_id: [
          { required: true, message: '上级部门不能为空', trigger: 'blur' }
        ],
        department_name: [
          { required: true, message: '部门名称不能为空', trigger: 'blur' }
        ],
        idx: [
          { required: true, message: '部门顺序不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    /** 查询部门列表 */
    getList() {
      this.loading = true
      getDeptList(this.queryParams).then(response => {
        this.deptList = response.data
        this.loading = false
      })
    },
    /** 转换部门数据结构 */
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
    /** 查询部门下拉树结构 */
    getTreeSelect() {
      getDeptList().then(response => {
        this.deptOptions = response.data
      })
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
        parent_id: undefined,
        department_name: undefined,
        idx: undefined,
        remarks: undefined
      }
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.getList()
    },
    /** 新增按钮操作 */
    handleAdd(row) {
      this.reset()
      this.getTreeSelect()
      if (row !== undefined) {
        this.form.parent_id = row.id
      }
      this.open = true
      this.title = '添加部门'
      this.isEdit = false
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      getDept({dept_id: row.id}).then(response => {
        this.form = response.data
        this.open = true
        this.title = '修改部门'
        this.isEdit = true
      })
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs['form'].validate(valid => {
        if (valid) {
          saveDept(this.form).then(response => {
            if (response.code === 200) {
              this.msgSuccess(response.message)
              this.open = false
              this.getList()
            } else {
              this.msgError(response.message)
            }
          })
        }
      })
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      this.$confirm(
        '是否确认删除名称为"' + row.department_name + '"的数据项?',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(function() {
          return delDept({dept_id: row.id})
        })
        .then(() => {
          this.getList()
          this.msgSuccess('删除成功，为不影响他人浏览，此操作将做不入库处理')
        })
        .catch(function() {})
    }
  }
}
</script>
