<template>
  <div class="rule-config">
    <el-card>
      <template #header>出题规则配置</template>

      <el-form v-loading="loading" :model="rules" label-width="200px">
        <el-divider>一年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade1.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade1.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最大结果">
              <el-input-number v-model="rules.grade1.maxResult" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>二年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade2.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade2.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最大结果">
              <el-input-number v-model="rules.grade2.maxResult" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>三年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade3.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade3.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="乘法数量">
              <el-input-number v-model="rules.grade3.multiplicationCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="最大结果">
              <el-input-number v-model="rules.grade3.maxResult" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>四年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade4.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade4.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="乘法数量">
              <el-input-number v-model="rules.grade4.multiplicationCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="除法数量">
              <el-input-number v-model="rules.grade4.divisionCount" :min="0" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>五年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="4">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade5.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade5.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="乘法数量">
              <el-input-number v-model="rules.grade5.multiplicationCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="除法数量">
              <el-input-number v-model="rules.grade5.divisionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="最大结果">
              <el-input-number v-model="rules.grade5.maxResult" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider>六年级</el-divider>
        <el-row :gutter="20">
          <el-col :span="4">
            <el-form-item label="加法数量">
              <el-input-number v-model="rules.grade6.additionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="减法数量">
              <el-input-number v-model="rules.grade6.subtractionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="乘法数量">
              <el-input-number v-model="rules.grade6.multiplicationCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="除法数量">
              <el-input-number v-model="rules.grade6.divisionCount" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="最大结果">
              <el-input-number v-model="rules.grade6.maxResult" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存配置</el-button>
          <el-button @click="fetchRules">重置</el-button>
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
const rules = reactive({
  grade1: { additionCount: 5, subtractionCount: 5, maxResult: 20 },
  grade2: { additionCount: 5, subtractionCount: 5, maxResult: 100 },
  grade3: { additionCount: 3, subtractionCount: 3, multiplicationCount: 4, maxResult: 100 },
  grade4: { additionCount: 3, subtractionCount: 3, multiplicationCount: 3, divisionCount: 1, maxResult: 1000 },
  grade5: { additionCount: 2, subtractionCount: 2, multiplicationCount: 2, divisionCount: 2, maxResult: 10000 },
  grade6: { additionCount: 2, subtractionCount: 2, multiplicationCount: 2, divisionCount: 2, maxResult: 10000 }
})

const fetchRules = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getRules()
    Object.assign(rules, res.data)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  await adminAPI.updateRules(rules)
  ElMessage.success('配置保存成功')
}

onMounted(fetchRules)
</script>
