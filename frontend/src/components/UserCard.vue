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
  padding: 1.5rem;
  background: white;
  border-radius: 20px;
  border: 1px solid #f0f0f0;
  gap: 1.5rem;
  min-width: 0;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.user-card.user-blocked {
  background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
  border-color: #feb2b2;
  box-shadow: 0 10px 30px rgba(245, 101, 101, 0.15);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 50%;
  font-size: 32px;
  flex-shrink: 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.user-blocked .user-avatar {
  background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
  color: #c53030;
  box-shadow: 0 4px 15px rgba(245, 101, 101, 0.2);
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.user-details h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  word-break: break-word;
}

.user-blocked .user-details h3 {
  color: #c53030;
}

.user-email {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
  word-break: break-all;
}

.user-blocked .user-email {
  color: #e53e3e;
}

.user-qualification {
  font-size: 0.875rem;
  color: #888;
  margin-top: 0.25rem;
  font-style: italic;
}

.blocked-indicator {
  font-size: 0.75rem;
  color: #c53030;
  font-weight: 600;
  margin-top: 0.5rem;
  background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  display: inline-block;
  width: fit-content;
  box-shadow: 0 2px 8px rgba(245, 101, 101, 0.2);
}

.user-actions {
  display: flex;
  align-items: center;
}

.toggle-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  min-width: 100px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.toggle-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.block-btn {
  background: linear-gradient(45deg, #dc3545 0%, #c82333 100%);
  color: white;
}

.block-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
}

.unblock-btn {
  background: linear-gradient(45deg, #28a745 0%, #218838 100%);
  color: white;
}

.unblock-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.loading-spinner {
  width: 18px;
  height: 18px;
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
    gap: 1rem;
    padding: 1rem;
  }
  
  .user-avatar {
    width: 48px;
    height: 48px;
    font-size: 24px;
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