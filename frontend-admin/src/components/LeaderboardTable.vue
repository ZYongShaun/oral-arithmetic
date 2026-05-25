<template>
  <el-table :data="tableData" border>
    <el-table-column prop="rank" label="排名" width="80">
      <template #default="{ row, $index }">
        <span v-if="row.icon">{{ row.icon }}</span>
        <span v-else>{{ row.rank || $index + 1 }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="username" label="用户名" />
    <el-table-column prop="question_count" label="答题数" width="120" />
    <el-table-column prop="score" label="得分" width="120" />
  </el-table>
</template>

<script setup>
defineProps({
  tableData: {
    type: Array,
    default: () => []
  }
})
</script>
