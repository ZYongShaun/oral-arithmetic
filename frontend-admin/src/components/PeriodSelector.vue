<template>
  <el-radio-group v-model="localPeriod" @change="onChange">
    <el-radio-button value="weekly">本周</el-radio-button>
    <el-radio-button value="monthly">本月</el-radio-button>
    <el-radio-button value="all">全部</el-radio-button>
  </el-radio-group>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'all'
  }
})

const emit = defineEmits(['update:modelValue'])

const localPeriod = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  localPeriod.value = newVal
})

const onChange = (val) => {
  emit('update:modelValue', val)
}
</script>
