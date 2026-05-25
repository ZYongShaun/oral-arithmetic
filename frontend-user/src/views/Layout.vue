<template>
  <div class="layout">
    <van-nav-bar
      :title="title"
      left-arrow
      @click-left="goBack"
      fixed
      placeholder
    />
    <div class="page-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const title = computed(() => router.currentRoute.value.meta.title || 'App')

const goBack = () => {
  if (window.history.length <= 1) {
    router.push('/')
  } else {
    router.back()
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: #f5f5f5;
}

.page-content {
  padding-bottom: 20px;
}
</style>
