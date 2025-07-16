<template>
  <div class="user-card">
    <div class="user-avatar">
      <span class="icon">👤</span>
    </div>
    <div class="user-details">
      <h3>{{ user.full_name }}</h3>
      <p class="user-email">{{ user.email }}</p>
      <p v-if="user.qualification" class="user-qualification">Qualification: {{ user.qualification }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
});
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
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-details h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #222;
  word-break: break-word;
}

.user-email {
  font-size: 14px;
  color: #666;
  margin-bottom: 2px;
  word-break: break-all;
}

.user-qualification {
  font-size: 13px;
  color: #888;
  margin-top: 2px;
  font-style: italic;
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
}
</style>