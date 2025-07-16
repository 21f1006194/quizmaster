<template>
  <div class="admin-users-dashboard">
    <div class="welcome-section">
      <div class="welcome-header">
        <h1>User Management</h1>
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
      (user.full_name && user.full_name.toLowerCase().includes(query))
    );
  });
};

onMounted(async () => {
  try {
    loading.value = true;
    const response = await api.get('/admin/api/all_users');
    users.value = response.data;
    filteredUsers.value = response.data;
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
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 16px 40px 16px;
}

.welcome-section {
  margin-bottom: 28px;
}

.welcome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-header h1 {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.search-section {
  margin-bottom: 24px;
}

.user-search-bar {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background-color: #f9f9f9;
  transition: border-color 0.2s;
}
.user-search-bar:focus {
  outline: none;
  border-color: #007bff;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin: 1rem 0;
}

.user-cards-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.user-cards {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.no-results {
  text-align: center;
  color: #888;
  margin-bottom: 18px;
}

@media (max-width: 768px) {
  .admin-users-dashboard {
    padding: 12px 4px 24px 4px;
  }
  .welcome-header h1 {
    font-size: 22px;
  }
  .user-cards {
    gap: 12px;
  }
}
</style>