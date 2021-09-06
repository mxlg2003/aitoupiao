<template>
  <BasicLayout>
    <template #wrapper>
      <el-card class="box-card">
        <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
          <el-form-item>
            <el-input
              v-model="queryParams.login_name"
              placeholder="请输入登录名"
              clearable
              style="width: 240px;"
              size="small"
              @keyup.enter.native="handleQuery"
            />
          </el-form-item>
          <el-form-item>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>

        <el-table v-loading="loading" :data="list">
          <el-table-column label="登录名" width="100" align="center" prop="login_name" />
          <el-table-column label="用户名" width="100" align="center" prop="user_name" />
          <el-table-column label="是否成功" align="center" width="80">
            <template slot-scope="scope">
              <span v-if="scope.row.is_success"> 成功 </span>
              <span v-else>失败</span>
            </template>
          </el-table-column>
          <el-table-column label="ip地址" align="center" prop="login_ip" width="110" />
          <el-table-column label="浏览器" align="center" prop="browser" :show-overflow-tooltip="true" />
          <el-table-column label="登录时间" align="center" prop="loginTime" width="180">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
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
      </el-card>
    </template>
  </BasicLayout>
</template>

<script>
import { loginList } from '@/api/system/log'

export default {
  data() {
    return {
      // 遮罩层
      loading: true,
      // 总条数
      total: 0,
      // 表格数据
      list: [],
      // 日期范围
      dateRange: [],
      // 查询参数
      queryParams: {
        page: 1,
        pageSize: 10,
        login_name: undefined
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    /** 查询登录日志列表 */
    getList() {
      this.loading = true
      if (this.dateRange) {
        this.queryParams.time_start = this.dateRange[0]
        this.queryParams.time_start = this.dateRange[1]
      } else {
        this.queryParams.time_start = ''
        this.queryParams.time_start = ''
      }
      loginList(this.queryParams).then(response => {
        this.list = response.data.log_list
        this.total = response.data.total
        this.loading = false
      }
      )
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
    }
  }
}
</script>

