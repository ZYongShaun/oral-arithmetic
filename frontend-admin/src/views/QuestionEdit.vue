<template>
  <div class="question-edit">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <el-button link @click="$router.back()">返回</el-button>
          <span>{{ isEdit ? '编辑题目' : '新建题目' }}</span>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="题目类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option label="加法" value="addition" />
            <el-option label="减法" value="subtraction" />
            <el-option label="乘法" value="multiplication" />
            <el-option label="除法" value="division" />
          </el-select>
        </el-form-item>

        <el-form-item label="年级" prop="grade">
          <el-select v-model="form.grade" placeholder="请选择">
            <el-option v-for="g in 6" :key="g" :label="`${g}年级`" :value="g" />
          </el-select>
        </el-form-item>

        <el-form-item label="数字A" prop="a">
          <el-input-number v-model="form.a" :min="1" :max="999" />
        </el-form-item>

        <el-form-item label="数字B" prop="b">
          <el-input-number v-model="form.b" :min="1" :max="999" />
        </el-form-item>

        <el-form-item label="答案" prop="answer">
          <el-input-number v-model="form.answer" />
        </el-form-item>

        <el-form-item label="难度" prop="difficulty">
          <el-rate v-model="form.difficulty" :max="5" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="disabled">禁用</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminAPI } from '@/apis/admin'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  type: 'addition',
  grade: 1,
  a: 1,
  b: 1,
  answer: 2,
  difficulty: 1,
  status: 'active'
})

const rules = {
  type: [{ required: true, message: '请选择题目类型', trigger: 'change' }],
  grade: [{ required: true, message: '请选择年级', trigger: 'change' }],
  a: [{ required: true, message: '请输入数字A', trigger: 'blur' }],
  b: [{ required: true, message: '请输入数字B', trigger: 'blur' }],
  answer: [{ required: true, message: '请输入答案', trigger: 'blur' }]
}

const fetchQuestion = async () => {
  if (isEdit.value) {
    const res = await adminAPI.getQuestions({ id: route.params.id })
    Object.assign(form, res.data.list[0])
  }
}

const handleSubmit = async () => {
  await formRef.value.validate()
  if (isEdit.value) {
    await adminAPI.updateQuestion(route.params.id, form)
    ElMessage.success('更新成功')
  } else {
    await adminAPI.createQuestion(form)
    ElMessage.success('创建成功')
  }
  router.back()
}

onMounted(fetchQuestion)
</script>
