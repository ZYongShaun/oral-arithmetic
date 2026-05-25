<template>
  <div class="star-shop-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <div class="header-content">
          <span>星星商城</span>
        </div>
      </template>
    </el-page-header>

    <el-card class="balance-card" shadow="never">
      <div class="balance-content">
        <div class="balance-display">
          <div class="balance-icon">
            <el-icon color="#FFD700" :size="60"><StarFilled /></el-icon>
          </div>
          <div class="balance-info">
            <div class="balance-label">当前星星</div>
            <div class="balance-value">{{ balance }}</div>
          </div>
        </div>
        <div class="balance-actions">
          <el-button type="primary" link @click="showTransactionsHistory">
            <el-icon><List /></el-icon>
            明细记录
          </el-button>
        </div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" class="shop-tabs">
      <el-tab-pane label="商城商品" name="items">
        <div class="shop-items" v-loading="loading">
          <div 
            v-for="item in shopItems" 
            :key="item.id"
            class="shop-item"
            :class="{ disabled: balance < item.price }"
          >
            <div class="item-image">
              <el-icon :size="80">
                <component :is="getItemIcon(item.type)" />
              </el-icon>
            </div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-desc">{{ item.description }}</div>
              <div class="item-price">
                <el-icon><StarFilled /></el-icon>
                <span class="price-value">{{ item.price }}</span>
              </div>
            </div>
            <div class="item-action">
              <el-button 
                type="primary" 
                size="large"
                :disabled="balance < item.price"
                @click="purchaseItem(item)"
              >
                {{ balance < item.price ? '星星不足' : '兑换' }}
              </el-button>
            </div>
          </div>
          
          <el-empty v-if="!loading && shopItems.length === 0" description="暂无商品" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="保护盾" name="shields">
        <div class="shield-shop" v-loading="loading">
          <div class="shield-item">
            <div class="shield-image">
              <el-icon color="#409eff" :size="100"><Shield /></el-icon>
            </div>
            <div class="shield-info">
              <div class="shield-name">保护盾</div>
              <div class="shield-desc">
                使用保护盾可以在忘记打卡时保持连续打卡天数
              </div>
              <div class="shield-price">
                <el-icon><StarFilled /></el-icon>
                <span class="price-value">50</span>
              </div>
            </div>
            <div class="shield-action">
              <el-button 
                type="primary" 
                size="large"
                :disabled="balance < 50"
                @click="purchaseShield"
              >
                {{ balance < 50 ? '星星不足' : '购买' }}
              </el-button>
            </div>
          </div>
          
          <el-card class="shield-info-card" shadow="never">
            <div class="shield-details">
              <div class="detail-item">
                <div class="detail-icon">
                  <el-icon><InfoFilled /></el-icon>
                </div>
                <div class="detail-text">
                  <div class="detail-title">使用规则</div>
                  <div class="detail-content">忘记打卡时自动消耗1个保护盾</div>
                </div>
              </div>
              
              <div class="detail-item">
                <div class="detail-icon">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="detail-text">
                  <div class="detail-title">叠加使用</div>
                  <div class="detail-content">可以购买多个保护盾，最多可累计7个</div>
                </div>
              </div>
              
              <div class="detail-item">
                <div class="detail-icon">
                  <el-icon><Timer /></el-icon>
                </div>
                <div class="detail-text">
                  <div class="detail-title">有效期</div>
                  <div class="detail-content">保护盾永久有效，不会过期</div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      v-model="showPurchaseDialog"
      title="确认购买"
      width="90%"
      :close-on-click-modal="false"
    >
      <div v-if="selectedItem" class="purchase-content">
        <div class="purchase-item">
          <div class="purchase-icon">
            <el-icon :size="48">
              <component :is="getItemIcon(selectedItem.type)" />
            </el-icon>
          </div>
          <div class="purchase-info">
            <div class="purchase-name">{{ selectedItem.name }}</div>
            <div class="purchase-price">
              <el-icon><StarFilled /></el-icon>
              <span>{{ selectedItem.price }}</span>
            </div>
          </div>
        </div>
        <el-alert
          title="购买后立即生效，星星将扣除"
          type="warning"
          :closable="false"
          show-icon
        />
      </div>
      
      <template #footer>
        <el-button @click="showPurchaseDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="purchaseLoading"
          @click="confirmPurchase"
        >
          确认购买
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showTransactionsDialog"
      title="星星明细"
      width="90%"
    >
      <div v-loading="transactionsLoading" class="transactions-list">
        <div 
          v-for="(item, index) in transactions" 
          :key="index"
          class="transaction-item"
        >
          <div class="transaction-info">
            <div class="transaction-desc">{{ item.description }}</div>
            <div class="transaction-time">{{ formatTime(item.createdAt) }}</div>
          </div>
          <div 
            class="transaction-amount"
            :class="{ positive: item.type === 'earn', negative: item.type === 'spend' }"
          >
            {{ item.type === 'earn' ? '+' : '-' }}{{ item.amount }}
          </div>
        </div>
        
        <el-empty 
          v-if="!transactionsLoading && transactions.length === 0" 
          description="暂无记录" 
        />
        
        <el-pagination
          v-if="totalTransactions > 0"
          v-model:current-page="transactionPage"
          :page-size="20"
          :total="totalTransactions"
          layout="prev, pager, next"
          small
          @current-change="loadTransactions"
          style="margin-top: 16px; text-align: center;"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStarBalance } from '@/apis/stars'
import { getShopItems, purchaseShopItem } from '@/apis/stars'
import { useShield } from '@/apis/streaks'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const purchaseLoading = ref(false)
const transactionsLoading = ref(false)
const childId = ref(null)
const activeTab = ref('items')
const balance = ref(0)
const showPurchaseDialog = ref(false)
const showTransactionsDialog = ref(false)
const selectedItem = ref(null)

const shopItems = ref([])
const transactions = ref([])
const transactionPage = ref(1)
const totalTransactions = ref(0)

const getItemIcon = (type) => {
  const icons = {
    'shield': 'Shield',
    'theme': 'Brush',
    'avatar': 'User',
    'title': 'Medal',
    'background': 'Picture'
  }
  return icons[type] || 'StarFilled'
}

const loadBalance = async () => {
  try {
    const response = await getStarBalance(childId.value)
    if (response.data) {
      balance.value = response.data.balance || 0
    }
  } catch (error) {
    console.error('加载星星余额失败:', error)
    ElMessage.error('加载星星余额失败')
  }
}

const loadShopItems = async () => {
  loading.value = true
  try {
    const response = await getShopItems()
    if (response.data && response.data.items) {
      shopItems.value = response.data.items.map(item => ({
        id: item.id,
        name: item.name,
        description: item.description,
        price: item.price || 0,
        type: item.type || 'shield'
      }))
    }
  } catch (error) {
    console.error('加载商品列表失败:', error)
    ElMessage.error('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

const purchaseItem = (item) => {
  if (balance.value < item.price) {
    ElMessage.warning('星星不足')
    return
  }
  
  selectedItem.value = item
  showPurchaseDialog.value = true
}

const confirmPurchase = async () => {
  if (!selectedItem.value) return
  
  purchaseLoading.value = true
  try {
    const response = await purchaseShopItem(selectedItem.value.id, {
      child_id: childId.value
    })
    if (response.code === 0 || response.status === 'success') {
      ElMessage.success('购买成功！')
      showPurchaseDialog.value = false
      loadBalance()
    } else {
      ElMessage.error(response.message || '购买失败')
    }
  } catch (error) {
    console.error('购买失败:', error)
    ElMessage.error(error.response?.data?.message || '购买失败')
  } finally {
    purchaseLoading.value = false
  }
}

const purchaseShield = async () => {
  if (balance.value < 50) {
    ElMessage.warning('星星不足')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      '确定要购买保护盾吗？花费50星星',
      '确认购买',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await useShield(childId.value, 50)
    if (response.code === 0 || response.status === 'success') {
      ElMessage.success('购买成功！')
      loadBalance()
    } else {
      ElMessage.error(response.message || '购买失败')
    }
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('购买保护盾失败:', error)
      ElMessage.error(error.response?.data?.message || '购买保护盾失败')
    }
  }
}

const showTransactionsHistory = () => {
  showTransactionsDialog.value = true
  loadTransactions()
}

const loadTransactions = async () => {
  transactionsLoading.value = true
  try {
    const response = await getStarTransactions(childId.value, {
      page: transactionPage.value,
      page_size: 20
    })
    if (response.data) {
      transactions.value = response.data.items || []
      totalTransactions.value = response.data.total || 0
    }
  } catch (error) {
    console.error('加载明细失败:', error)
    ElMessage.error('加载明细失败')
  } finally {
    transactionsLoading.value = false
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

onMounted(() => {
  childId.value = parseInt(route.query.childId) || parseInt(localStorage.getItem('lastSelectedChildId'))
  if (!childId.value) {
    ElMessage.error('缺少孩子ID')
    router.back()
    return
  }
  
  loadBalance()
  loadShopItems()
})
</script>

<style scoped lang="scss">
.star-shop-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.balance-card {
  border-radius: 12px;
  margin: 16px;
  
  .balance-content {
    .balance-display {
      display: flex;
      align-items: center;
      gap: 20px;
      
      .balance-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #fff9c4 0%, #ffecb3 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .balance-info {
        flex: 1;
        
        .balance-label {
          font-size: 14px;
          color: #999;
          margin-bottom: 4px;
        }
        
        .balance-value {
          font-size: 36px;
          font-weight: bold;
          background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
      }
    }
    
    .balance-actions {
      text-align: right;
      padding-top: 8px;
      border-top: 1px solid #eee;
      margin-top: 12px;
    }
  }
}

.shop-tabs {
  background: white;
  margin: 16px;
  border-radius: 12px;
  padding: 16px;
  
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
}

.shop-items {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  
  .shop-item {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, opacity 0.2s;
    
    &.disabled {
      opacity: 0.5;
    }
    
    &:active {
      transform: scale(0.98);
    }
    
    .item-image {
      text-align: center;
      padding: 20px 0;
      color: #667eea;
    }
    
    .item-info {
      text-align: center;
      margin-bottom: 16px;
      
      .item-name {
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
      }
      
      .item-desc {
        font-size: 12px;
        color: #999;
        margin-bottom: 12px;
        line-height: 1.5;
        min-height: 36px;
      }
      
      .item-price {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        padding: 8px 16px;
        background: linear-gradient(135deg, #fff9c4 0%, #ffecb3 100%);
        border-radius: 20px;
        
        .el-icon {
          color: #FFD700;
        }
        
        .price-value {
          font-size: 18px;
          font-weight: bold;
          color: #FFA500;
        }
      }
    }
    
    .item-action {
      .el-button {
        width: 100%;
        height: 44px;
        border-radius: 8px;
      }
    }
  }
}

.shield-shop {
  .shield-item {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-radius: 16px;
    padding: 32px 20px;
    text-align: center;
    margin-bottom: 16px;
    
    .shield-image {
      margin-bottom: 16px;
      color: #409eff;
    }
    
    .shield-info {
      margin-bottom: 20px;
      
      .shield-name {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
      }
      
      .shield-desc {
        font-size: 14px;
        color: #666;
        margin-bottom: 16px;
        line-height: 1.6;
      }
      
      .shield-price {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 10px 24px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        
        .el-icon {
          color: #FFD700;
        }
        
        .price-value {
          font-size: 24px;
          font-weight: bold;
          color: #FFA500;
        }
      }
    }
    
    .shield-action {
      .el-button {
        width: 100%;
        height: 50px;
        font-size: 16px;
        border-radius: 12px;
      }
    }
  }
  
  .shield-info-card {
    .shield-details {
      .detail-item {
        display: flex;
        gap: 12px;
        padding: 16px 0;
        border-bottom: 1px solid #eee;
        
        &:last-child {
          border-bottom: none;
        }
        
        .detail-icon {
          width: 40px;
          height: 40px;
          border-radius: 8px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          flex-shrink: 0;
        }
        
        .detail-text {
          flex: 1;
          
          .detail-title {
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 4px;
          }
          
          .detail-content {
            font-size: 12px;
            color: #999;
            line-height: 1.5;
          }
        }
      }
    }
  }
}

.purchase-content {
  .purchase-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 12px;
    margin-bottom: 16px;
    
    .purchase-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    
    .purchase-info {
      flex: 1;
      
      .purchase-name {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
      }
      
      .purchase-price {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 20px;
        font-weight: bold;
        color: #FFA500;
      }
    }
  }
}

.transactions-list {
  max-height: 400px;
  overflow-y: auto;
  
  .transaction-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
    
    .transaction-info {
      flex: 1;
      
      .transaction-desc {
        font-size: 14px;
        color: #333;
        margin-bottom: 4px;
      }
      
      .transaction-time {
        font-size: 12px;
        color: #999;
      }
    }
    
    .transaction-amount {
      font-size: 18px;
      font-weight: bold;
      
      &.positive {
        color: #67c23a;
      }
      
      &.negative {
        color: #f56c6c;
      }
    }
  }
}

@media (max-width: 768px) {
  .shop-items {
    grid-template-columns: 1fr;
  }
}
</style>
