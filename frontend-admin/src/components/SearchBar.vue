<template>
  <el-input
    v-model="localQuery"
    placeholder="搜索..."
    clearable
    @clear="handleClear"
    @keyup.enter="handleSearch"
  >
    <template #append>
      <el-button @click="handleSearch">搜索</el-button>
    </template>
  </el-input>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'search'])

const localQuery = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  localQuery.value = newVal
})

const handleSearch = () => {
  emit('update:modelValue', localQuery.value)
  emit('search')
}

const handleClear = () => {
  localQuery.value = ''
  emit('update:modelValue', '')
  emit('search')
}
</script>
