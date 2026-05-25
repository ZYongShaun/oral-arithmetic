<template>
  <div class="system-config">
    <el-card>
      <template #header>系统配置</template>

      <el-form v-loading="loading" :model="config" label-width="150px">
        <el-divider>每日任务配置</el-divider>
        <el-form-item label="每日任务数量">
          <el-input-number v-model="config.dailyTaskCount" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="任务时间限制(秒)">
          <el-input-number v-model="config.dailyTaskTimeLimit" :min="10" />
        </el-form-item>
        <el-form-item label="每日星星上限">
          <el-input-number v-model="config.dailyStarLimit" :min="1" />
        </el-form-item>

        <el-divider>星星奖励配置</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="正确率>90%">
              <el-input-number v-model="config.starRewards.excellent" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="正确率>80%">
              <el-input-number v-model="config.starRewards.good" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="正确率>60%">
              <el-input-number v-model="config.starRewards.normal" :min="0" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>保护罩配置</el-divider>
        <el-form-item label="保护罩价格(星星)">
          <el-input-number v-model="config.shieldPrice" :min="0" />
        </el-form-item>
        <el-form-item label="保护罩持续时间(小时)">
          <el-input-number v-model="config.shieldDuration" :min="1" />
        </el-form-item>

        <el-divider>其他配置</el-divider>
        <el-form-item label="排行榜显示数量">
          <el-input-number v-model="config.leaderboardLimit" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="练习记录保留天数">
          <el-input-number v-model="config.recordRetentionDays" :min="1" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存配置</el-button>
          <el-button @click="fetchConfig">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminAPI } from '@/apis/admin'

const loading = ref(false)
const config = reactive({
  dailyTaskCount: 20,
  dailyTaskTimeLimit: 300,
  dailyStarLimit: 100,
  starRewards: {
    excellent: 3,
    good: 2,
    normal: 1
  },
  shieldPrice: 50,
  shieldDuration: 24,
  leaderboardLimit: 50,
  recordRetentionDays: 90
})

const fetchConfig = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getConfigs()
    Object.assign(config, res.data)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  await adminAPI.updateConfigs(config)
  ElMessage.success('配置保存成功')
}

onMounted(fetchConfig)
</script>
