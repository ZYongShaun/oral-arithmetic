<template>
  <div class="question-import">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <el-button link @click="$router.back()">返回</el-button>
          <span>批量导入题目</span>
        </div>
      </template>

      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :limit="1"
        :on-change="handleFileChange"
        drag
        accept=".xlsx,.xls,.csv"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传 xlsx/xls/csv 文件，且不超过 10MB
          </div>
        </template>
      </el-upload>

      <el-divider />

      <el-descriptions title="文件格式说明" :column="1" border>
        <el-descriptions-item label="题目类型">
          加法/addition、减法/subtraction、乘法/multiplication、除法/division
        </el-descriptions-item>
        <el-descriptions-item label="年级">1-6</el-descriptions-item>
        <el-descriptions-item label="数字A">第一个数字</el-descriptions-item>
        <el-descriptions-item label="数字B">第二个数字</el-descriptions-item>
        <el-descriptions-item label="答案">计算结果</el-descriptions-item>
        <el-descriptions-item label="难度">1-5</el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <el-button type="primary" @click="handleDownloadTemplate">下载模板</el-button>
      <el-button type="success" @click="handleImport" :disabled="!file">开始导入</el-button>
    </el-card>

    <el-dialog v-model="resultVisible" title="导入结果" width="600px">
      <el-result
        :icon="importResult.success ? 'success' : 'error'"
        :title="importResult.success ? '导入成功' : '导入失败'"
      >
        <template #sub-title>
          <p>成功导入 {{ importResult.successCount }} 条数据</p>
          <p v-if="importResult.failedCount > 0">失败 {{ importResult.failedCount }} 条数据</p>
          <el-alert
            v-if="importResult.errors && importResult.errors.length > 0"
            title="错误详情"
            type="error"
            :closable="false"
            style="margin-top: 10px"
          >
            <ul>
              <li v-for="(error, index) in importResult.errors" :key="index">{{ error }}</li>
            </ul>
          </el-alert>
        </template>
        <template #extra>
          <el-button type="primary" @click="resultVisible = false">确定</el-button>
        </template>
      </el-result>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, UploadFilled } from '@element-plus/icons-vue'
import { adminAPI } from '@/apis/admin'

const router = useRouter()
const uploadRef = ref(null)
const file = ref(null)
const importResult = ref({
  success: false,
  successCount: 0,
  failedCount: 0,
  errors: []
})
const resultVisible = ref(false)

const handleFileChange = (uploadFile) => {
  file.value = uploadFile.raw
}

const handleDownloadTemplate = () => {
  const link = document.createElement('a')
  link.href = '/template/question-template.xlsx'
  link.download = '题目导入模板.xlsx'
  link.click()
}

const handleImport = async () => {
  if (!file.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const res = await adminAPI.batchImportQuestions(formData)
    importResult.value = res.data
    resultVisible.value = true
    if (res.data.success) {
      setTimeout(() => {
        router.back()
      }, 2000)
    }
  } catch (error) {
    importResult.value = {
      success: false,
      successCount: 0,
      failedCount: 1,
      errors: [error.message || '导入失败']
    }
    resultVisible.value = true
  }
}
</script>

<style scoped>
.el-icon--upload {
  font-size: 67px;
  color: var(--el-text-color-secondary);
  margin: 40px 0 16px;
}
</style>
