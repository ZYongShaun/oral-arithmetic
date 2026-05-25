<template>
  <el-card shadow="hover">
    <el-statistic :title="title" :value="value">
      <template #suffix>{{ suffix }}</template>
    </el-statistic>
  </el-card>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    default: 0
  },
  suffix: {
    type: String,
    default: ''
  }
})
</script>
