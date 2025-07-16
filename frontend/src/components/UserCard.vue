<template>
  <div class="user-card" :class="{ 'user-blocked': user.isBlocked }">
    <div class="user-avatar">
      <span class="icon">👤</span>
    </div>
    <div class="user-details">
      <h3>{{ user.full_name }}</h3>
      <p class="user-email">{{ user.email }}</p>
      <p v-if="user.qualification" class="user-qualification">Qualification: {{ user.qualification }}</p>
      <p v-if="user.isBlocked" class="blocked-indicator">🚫 Blocked User</p>
    </div>
    <div class="user-actions">
      <button 
        class="toggle-btn"
        :class="user.isBlocked ? 'unblock-btn' : 'block-btn'" 
        @click="toggleBlockStatus"
        :disabled="isLoading"
      >
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>{{ user.isBlocked ? 'Unblock' : 'Block' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/api';

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
});

const isLoading = ref(false);

const toggleBlockStatus = async () => {
  isLoading.value = true;
  try {
    if (props.user.isBlocked) {
      const response = await unblockUser(props.user.id);
      if (response) {
        props.user.isBlocked = false;
        props.user.keywords = '';
      }
    } else {
      const response = await blockUser(props.user.id);
      if (response) {
        props.user.isBlocked = true;
        props.user.keywords = 'blocked';
      }
    }
  } catch (error) {
    console.error('Error toggling user block status:', error);
  } finally {
    isLoading.value = false;
  }
};

const blockUser = async (user_id) => {
  try {
    const response = await api.post(`/admin/api/block_user/${user_id}`);
    if (response.status === 200) {
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error blocking user:', error);
    return false;
  }
};

const unblockUser = async (user_id) => {
  try {
    const response = await api.post(`/admin/api/unblock_user/${user_id}`);
    if (response.status === 200) {
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error unblocking user:', error);
    return false;
  }
};

</script>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  gap: 18px;
  min-width: 0;
  transition: all 0.3s ease;
  position: relative;
}

.user-card.user-blocked {
  background-color: #fff5f5;
  border-color: #fed7d7;
  box-shadow: 0 2px 4px rgba(245, 101, 101, 0.1);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: #e9ecef;
  border-radius: 50%;
  font-size: 28px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.user-blocked .user-avatar {
  background-color: #fed7d7;
  color: #c53030;
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.user-details h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #222;
  word-break: break-word;
}

.user-blocked .user-details h3 {
  color: #c53030;
}

.user-email {
  font-size: 14px;
  color: #666;
  margin-bottom: 2px;
  word-break: break-all;
}

.user-blocked .user-email {
  color: #e53e3e;
}

.user-qualification {
  font-size: 13px;
  color: #888;
  margin-top: 2px;
  font-style: italic;
}

.blocked-indicator {
  font-size: 12px;
  color: #c53030;
  font-weight: 500;
  margin-top: 4px;
  background-color: #fed7d7;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
  width: fit-content;
}

.user-actions {
  display: flex;
  align-items: center;
}

.toggle-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  min-width: 80px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.block-btn {
  background-color: #dc3545;
  color: white;
}

.block-btn:hover:not(:disabled) {
  background-color: #c82333;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
}

.unblock-btn {
  background-color: #28a745;
  color: white;
}

.unblock-btn:hover:not(:disabled) {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .user-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    font-size: 22px;
  }
  
  .user-actions {
    align-self: stretch;
  }
  
  .toggle-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>