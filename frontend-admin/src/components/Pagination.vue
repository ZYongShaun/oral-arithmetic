<template>
  <el-pagination
    v-model:current-page="innerCurrentPage"
    v-model:page-size="innerPageSize"
    :total="total"
    :page-sizes="pageSizes"
    :layout="layout"
    @current-change="onCurrentChange"
    @size-change="onSizeChange"
  />
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ page: 1, pageSize: 20 })
  },
  total: {
    type: Number,
    default: 0
  },
  pageSizes: {
    type: Array,
    default: () => [20, 50, 100]
  },
  layout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const innerCurrentPage = ref(props.modelValue.page)
const innerPageSize = ref(props.modelValue.pageSize)

watch(() => props.modelValue.page, (newVal) => {
  innerCurrentPage.value = newVal
})
watch(() => props.modelValue.pageSize, (newVal) => {
  innerPageSize.value = newVal
})

const onCurrentChange = (val) => {
  emit('update:modelValue', { ...props.modelValue, page: val })
  emit('change')
}
const onSizeChange = (val) => {
  innerPageSize.value = val
  emit('update:modelValue', { ...props.modelValue, pageSize: val, page: 1 })
  emit('change')
}
</script>
