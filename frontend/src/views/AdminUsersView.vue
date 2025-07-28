<template>
  <div class="admin-users-dashboard">
    <div class="container">
      <div class="welcome-section">
        <div class="welcome-header">
          <h1 class="dashboard-title">User Management</h1>
        </div>
      </div>

      <div class="search-section">
        <input
          v-model="searchQuery"
          type="text"
          class="user-search-bar"
          placeholder="Search users by username, email, or full name..."
          @input="filterUsers"
        />
      </div>

      <div v-if="loading" class="loading-state">
        <p>Loading users...</p>
      </div>
      <div v-else class="user-cards-section">
        <div v-if="filteredUsers.length === 0" class="no-results">
          <p>No users found.</p>
        </div>
        <div class="user-cards">
          <UserCard v-for="user in filteredUsers" :key="user.id" :user="user" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import UserCard from '../components/UserCard.vue';
import api from '@/api';

const users = ref([]);
const filteredUsers = ref([]);
const searchQuery = ref('');
const loading = ref(true);

const filterUsers = () => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) {
    filteredUsers.value = users.value;
    return;
  }
  filteredUsers.value = users.value.filter(user => {
    return (
      (user.username && user.username.toLowerCase().includes(query)) ||
      (user.email && user.email.toLowerCase().includes(query)) ||
      (user.full_name && user.full_name.toLowerCase().includes(query)) ||
      (user.keywords && user.keywords.toLowerCase().includes(query))
    );
  });
};

onMounted(async () => {
  try {
    loading.value = true;
    const response = await api.get('/admin/api/all_users');
    // Add keywords field to each user
    const usersWithKeywords = response.data.map(user => ({
      ...user,
      keywords: user.isBlocked ? 'blocked' : ''
    }));
    users.value = usersWithKeywords;
    filteredUsers.value = usersWithKeywords;
  } catch (error) {
    console.error('Failed to fetch users:', error);
    users.value = [];
    filteredUsers.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.admin-users-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.welcome-section {
  margin-bottom: 2rem;
}

.welcome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
}

.search-section {
  margin-bottom: 2rem;
}

.user-search-bar {
  width: 100%;
  padding: 1rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  font-size: 1rem;
  background-color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.user-search-bar:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}

.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  margin: 1rem 0;
}

.user-cards-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.user-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.no-results {
  text-align: center;
  color: #666;
  margin-bottom: 1.5rem;
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-title {
    font-size: 2rem;
  }
  
  .admin-users-dashboard {
    padding: 1rem 0;
  }
  
  .welcome-header {
    padding: 1rem;
  }
  
  .container {
    padding: 0 15px;
  }
  
  .user-cards {
    gap: 1rem;
  }
}
</style>