<template>
  <div class="content">
    <el-tabs v-model="activeName" @tab-click="handleClick" style="padding-left: 30px;">
      <el-tab-pane label="全部" name="first">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="进行中" name="second">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="未开始" name="third">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="已结束" name="fourth">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="审核中" name="five">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="违规" name="six">
        <el-table v-loading="loading" :data="activityList">
          <el-table-column prop="department_name" label="活动海报" />
          <el-table-column prop="idx" label="活动标题" width="200" />
          <el-table-column label="活动时间" align="center" prop="create_time" width="200">
            <template slot-scope="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button size="mini" type="text" icon="el-icon-edit">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>

export default {
  name: 'Dept',
  data() {
    return {
      loading: false,
      activeName: 'first',
      activityList: [],
      total: 0,
      queryParams: {
        page: 1,
        pageSize: 10
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    handleClick(tab, event) {
      this.activeName = tab.name
      this.getList()
    },
    // 获取列表信息
    getList() {

    }
  }
}
</script>
<style lang="scss" scoped>
  .content{
    background: #ffffff;
  }
</style>
