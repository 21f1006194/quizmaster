<template>
  <div class="leaderboard-container">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading leaderboard...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <h3>Error</h3>
        <p>{{ error }}</p>
        <button @click="loadLeaderboard" class="retry-btn">Retry</button>
      </div>
    </div>

    <div v-else-if="leaderboard" class="leaderboard-content">
      <!-- Quiz Information Header -->
      <div class="quiz-header">
        <h1>{{ leaderboard.quiz.title }}</h1>
        <div class="quiz-details">
          <div class="detail-item">
            <span class="label">Subject:</span>
            <span class="value">{{ leaderboard.quiz.subject_name }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Chapter:</span>
            <span class="value">{{ leaderboard.quiz.chapter_name }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Duration:</span>
            <span class="value">{{ leaderboard.quiz.time_duration }} minutes</span>
          </div>
          <div class="detail-item">
            <span class="label">Date:</span>
            <span class="value">{{ formatDate(leaderboard.quiz.quiz_date) }}</span>
          </div>
          <div v-if="leaderboard.quiz.remarks" class="detail-item">
            <span class="label">Remarks:</span>
            <span class="value">{{ leaderboard.quiz.remarks }}</span>
          </div>
        </div>
        <div class="participants-count">
          <span>{{ leaderboard.total_participants }} participant{{ leaderboard.total_participants !== 1 ? 's' : '' }}</span>
        </div>
      </div>

      <!-- Leaderboard Table -->
      <div class="leaderboard-table-container">
        <h2>Leaderboard</h2>
        <div v-if="leaderboard.leaderboard.length === 0" class="no-participants">
          <p>No participants yet</p>
        </div>
        <div v-else class="leaderboard-table">
          <div class="table-header">
            <div class="rank-col">Rank</div>
            <div class="user-col">User</div>
            <div class="score-col">Score</div>
            <div class="time-col">Completion Time</div>
            <div class="duration-col">Duration</div>
          </div>
          
          <div 
            v-for="entry in leaderboard.leaderboard" 
            :key="entry.user_id"
            class="table-row"
            :class="{ 'top-three': entry.rank <= 3 }"
          >
            <div class="rank-col">
              <div class="rank-badge" :class="getRankClass(entry.rank)">
                {{ entry.rank }}
              </div>
            </div>
            <div class="user-col">
              <div class="user-info">
                <div class="username">{{ entry.username }}</div>
                <div class="full-name">{{ entry.full_name }}</div>
              </div>
            </div>
            <div class="score-col">
              <span class="score">{{ entry.score }}</span>
            </div>
            <div class="time-col">
              {{ formatDateTime(entry.end_time) }}
            </div>
            <div class="duration-col">
              {{ calculateDuration(entry.start_time, entry.end_time) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";

const loading = ref(false);
const error = ref(null);
const leaderboard = ref(null);

const props = defineProps({
  quizId: {
    type: Number,
    required: true,
  },
});

const loadLeaderboard = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await api.get(`/user/api/quiz/${props.quizId}/leaderboard`);
    leaderboard.value = response.data;
  } catch (err) {
    console.error('Error loading leaderboard:', err);
    error.value = err.response?.data?.message || 'Failed to load leaderboard';
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const calculateDuration = (startTime, endTime) => {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diffMs = end - start;
  const minutes = Math.floor(diffMs / 60000);
  const seconds = Math.floor((diffMs % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
};

const getRankClass = (rank) => {
  if (rank === 1) return 'gold';
  if (rank === 2) return 'silver';
  if (rank === 3) return 'bronze';
  return 'normal';
};

onMounted(() => {
  loadLeaderboard();
});
</script>

<style scoped>
.leaderboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-message {
  text-align: center;
  padding: 20px;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
}

.retry-btn {
  margin-top: 10px;
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #2980b9;
}

.leaderboard-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.quiz-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  text-align: center;
}

.quiz-header h1 {
  margin: 0 0 20px 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.quiz-details {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.label {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 4px;
}

.value {
  font-weight: 600;
  font-size: 1.1rem;
}

.participants-count {
  font-size: 1.2rem;
  opacity: 0.9;
}

.leaderboard-table-container {
  padding: 30px;
}

.leaderboard-table-container h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.8rem;
}

.no-participants {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

.leaderboard-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: grid;
  grid-template-columns: 80px 2fr 1fr 1fr 1fr;
  background: #f8f9fa;
  padding: 15px 20px;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
}

.table-row {
  display: grid;
  grid-template-columns: 80px 2fr 1fr 1fr 1fr;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.table-row:hover {
  background-color: #f8f9fa;
}

.table-row.top-three {
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%);
}

.rank-col {
  display: flex;
  align-items: center;
}

.rank-badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.rank-badge.gold {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #b8860b;
}

.rank-badge.silver {
  background: linear-gradient(135deg, #c0c0c0, #e5e5e5);
  color: #696969;
}

.rank-badge.bronze {
  background: linear-gradient(135deg, #cd7f32, #daa520);
  color: #8b4513;
}

.rank-badge.normal {
  background: #6c757d;
  color: white;
}

.user-col {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 600;
  color: #333;
  font-size: 1.1rem;
}

.full-name {
  color: #666;
  font-size: 0.9rem;
}

.score-col {
  display: flex;
  align-items: center;
  font-weight: 600;
}

.score {
  font-size: 1.3rem;
  color: #28a745;
}

.time-col, .duration-col {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .leaderboard-container {
    padding: 10px;
  }
  
  .quiz-header {
    padding: 20px;
  }
  
  .quiz-header h1 {
    font-size: 2rem;
  }
  
  .quiz-details {
    gap: 15px;
  }
  
  .detail-item {
    min-width: 100px;
  }
  
  .leaderboard-table-container {
    padding: 20px;
  }
  
  .table-header, .table-row {
    grid-template-columns: 60px 1fr 80px;
    padding: 10px 15px;
  }
  
  .time-col, .duration-col {
    display: none;
  }
  
  .table-header div:nth-child(4),
  .table-header div:nth-child(5),
  .table-row div:nth-child(4),
  .table-row div:nth-child(5) {
    display: none;
  }
}
</style>