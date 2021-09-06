<template>
  <BasicLayout>
    <template #wrapper>
      <el-card class="box-card">
        <el-form :inline="true">
          <el-form-item>
            <el-input
              v-model="queryParams.menu_name"
              placeholder="请输入菜单名称"
              clearable
              size="small"
              @keyup.enter.native="handleQuery"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
            <el-button
              v-permisaction="['system:sysmenu:add']"
              type="primary"
              icon="el-icon-plus"
              size="mini"
              @click="handleAdd"
            >新增</el-button>
          </el-form-item>
        </el-form>

        <el-table
          v-loading="loading"
          :data="menuList"
          row-key="id"
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
        >
          <el-table-column prop="menu_name" label="菜单名称" :show-overflow-tooltip="true" width="180px" />
          <el-table-column prop="menu_code" label="图标" align="center" width="100px">
            <template slot-scope="scope">
              <svg-icon :icon-class="scope.row.menu_icon" />
            </template>
          </el-table-column>
          <el-table-column prop="idx" label="排序" width="60px" />
          <el-table-column prop="menu_url" label="权限标识" :show-overflow-tooltip="true" />
          <el-table-column prop="menu_code" label="组件路径" :show-overflow-tooltip="true" />
          <el-table-column label="权限类型" align="center" prop="createdAt" width="180">
            <template slot-scope="scope">
              <span v-if="scope.row.menu_type === 0">目录</span>
              <span v-else-if="scope.row.menu_type === 1">菜单</span>
              <span v-else-if="scope.row.menu_type === 3">外链</span>
              <span v-else>按钮</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="180">
            <template slot-scope="scope">
              <el-button
                v-permisaction="['system:sysmenu:edit']"
                size="mini"
                type="text"
                icon="el-icon-edit"
                @click="handleUpdate(scope.row)"
              >修改</el-button>
              <el-button
                v-if="scope.row.menu_type === 0 || scope.row.menu_type === 1"
                v-permisaction="['system:sysmenu:add']"
                size="mini"
                type="text"
                icon="el-icon-plus"
                @click="handleAdd(scope.row)"
              >新增</el-button>
              <el-button
                v-permisaction="['system:sysmenu:remove']"
                size="mini"
                type="text"
                icon="el-icon-delete"
                @click="handleDelete(scope.row)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 添加或修改菜单对话框 -->
        <el-dialog :title="title" :visible.sync="open" width="600px">
          <el-form ref="form" :model="form" :rules="rules" label-width="80px">
            <el-row>
              <el-col :span="24">
                <el-form-item label="上级菜单">
                  <TreeSelect
                    v-model="form.parent_id"
                    :options="menuOptions"
                    :normalizer="normalizer"
                    :show-count="true"
                    placeholder="选择上级菜单"
                    :disabled="form.id ? true : false"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="菜单名称" prop="menu_name">
                  <el-input v-model="form.menu_name" placeholder="请输入菜单名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="显示排序" prop="idx">
                  <el-input-number v-model="form.idx" controls-position="right" :min="0" />
                </el-form-item>
              </el-col>

              <el-col :span="24">
                <el-form-item label="菜单类型" prop="menu_type">
                  <el-radio-group v-model="form.menu_type">
                    <el-radio label="0">目录</el-radio>
                    <el-radio label="1">菜单</el-radio>
                    <el-radio label="2">按钮</el-radio>
                    <el-radio label="3">外链</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="菜单图标">
                  <el-popover
                    placement="bottom-start"
                    width="460"
                    trigger="click"
                    @show="$refs['iconSelect'].reset()"
                  >
                    <IconSelect ref="iconSelect" @selected="selected" />
                    <el-input slot="reference" v-model="form.menu_icon" placeholder="点击选择图标" readonly>
                      <svg-icon
                        v-if="form.menu_icon"
                        slot="prefix"
                        :icon-class="form.menu_icon"
                        class="el-input__icon"
                        style="height: 32px;width: 16px;"
                      />
                      <i v-else slot="prefix" class="el-icon-search el-input__icon" />
                    </el-input>
                  </el-popover>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="组件路径" prop="menu_code">
                  <el-input v-if="form.menu_type === '0'" value="Layout" disabled />
                  <el-input v-else v-model="form.menu_code" placeholder="请输入组件路径" />
                </el-form-item>
              </el-col>

              <el-col :span="12">
                <el-form-item label="权限标识" prop="menu_url">
                  <el-input v-model="form.menu_url" placeholder="请输入权限标识" />
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
import { getMenuList, getMenu, delMenu, saveMenu } from '@/api/system/menu'
import TreeSelect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import IconSelect from '@/components/IconSelect/index'

export default {
  name: 'Menu',
  components: { TreeSelect, IconSelect },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 菜单表格树数据
      menuList: [],
      // 菜单树选项
      menuOptions: [],
      // 弹出层标题
      title: '',
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        menu_name: undefined
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        menu_name: [
          { required: true, message: '菜单名称不能为空', trigger: 'blur' }
        ],
        idx: [
          { required: true, message: '菜单顺序不能为空', trigger: 'blur' }
        ],
        menu_type: [
          { required: true, message: '菜单类型不能为空', trigger: 'blur' }
        ],
        menu_url: [
          { required: true, message: '权限标识不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    // 选择图标
    selected(name) {
      this.$set(this.form, 'menu_icon', name)
    },
    /** 查询菜单列表 */
    getList() {
      this.loading = true
      getMenuList(this.queryParams).then(response => {
        this.menuList = response.data
        this.loading = false
      })
    },
    // 处理树形结构的菜单
    getMenuTree() {
      this.menuOptions = this.menuList
    },
    /** 转换菜单数据结构 */
    normalizer(node) {
      if (node.children && !node.children.length) {
        delete node.children
      }
      return {
        id: node.id,
        label: node.menu_name,
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
        parent_id: undefined,
        menu_name: undefined,
        menu_url: undefined,
        menu_code: undefined,
        menu_icon: undefined,
        menu_type: '0',
        idx: 0
      }
      this.resetForm('form')
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.getList()
    },
    /** 新增按钮操作 */
    handleAdd(row) {
      this.reset()
      if (row != null) {
        this.form.parent_id = row.id
      }
      this.getMenuTree()
      this.open = true
      this.title = '添加菜单'
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset()
      this.getMenuTree()
      getMenu({ menu_id: row.id }).then(response => {
        this.form = response.data
        this.form.menu_type = this.form.menu_type.toString()
        this.open = true
        this.title = '修改菜单'
      })
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs['form'].validate(valid => {
        if (this.form.menu_type === '0') {
          this.form.menu_code = 'Layout'
        }
        if (valid) {
          saveMenu(this.form).then(response => {
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
      this.$confirm('是否确认删除名称为"' + row.menu_name + '"的数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return delMenu({ menu_id: row.id })
      }).then(() => {
        this.getList()
        this.msgSuccess('删除成功，为不影响他人浏览，此操作将做不入库处理')
      }).catch(function() {})
    }
  }
}
</script>
