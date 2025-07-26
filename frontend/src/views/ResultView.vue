<template>
  <div class="score-view">
    <div class="score-header">
      <h1>Quiz Results</h1>
      <p>View your quiz results history.</p>
    </div>

    <!-- Search Bar -->
    <div class="search-section">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by subject, chapter, or quiz title..."
          class="search-input"
          @input="filterResults"
        />
        <i class="bi bi-search search-icon"></i>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading your quiz history...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="alert alert-danger">
        <i class="bi bi-exclamation-triangle"></i>
        {{ error }}
      </div>
      <button @click="loadQuizHistory" class="btn btn-primary retry-btn">
        <i class="bi bi-arrow-clockwise"></i> Retry
      </button>
    </div>

    <!-- Results -->
    <div v-else class="results-section">
      <div v-if="filteredHistory.length === 0" class="no-results">
        <div class="no-results-content">
          <i class="bi bi-inbox"></i>
          <h3>No quiz attempts found</h3>
          <p v-if="searchQuery">
            No results match your search: "{{ searchQuery }}"
          </p>
          <p v-else>
            You haven't completed any quizzes yet.
          </p>
        </div>
      </div>

      <div v-else>
        <div class="results-summary">
          <p>Showing {{ filteredHistory.length }} of {{ quizHistory.length }} attempts</p>
        </div>
        
        <ScoreTable 
          :quiz-history="filteredHistory"
          @view-result="viewResult"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import ScoreTable from '@/components/ScoreTable.vue';

const router = useRouter();

// Data refs
const quizHistory = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');

// Computed property for filtered results
const filteredHistory = computed(() => {
  if (!searchQuery.value.trim()) {
    return quizHistory.value;
  }
  
  const query = searchQuery.value.toLowerCase();
  return quizHistory.value.filter(attempt => 
    attempt.subject_name.toLowerCase().includes(query) ||
    attempt.chapter_name.toLowerCase().includes(query) ||
    attempt.quiz_title.toLowerCase().includes(query)
  );
});

// Load quiz history from API
const loadQuizHistory = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await api.get('/user/api/quiz/history');
    quizHistory.value = response.data;
  } catch (err) {
    console.error('Error loading quiz history:', err);
    error.value = err.response?.data?.message || 'Failed to load quiz history';
  } finally {
    loading.value = false;
  }
};

// Filter results when search query changes
const filterResults = () => {
  // The computed property handles the filtering automatically
};

// Navigate to quiz result view
const viewResult = (attemptId) => {
  const attempt = quizHistory.value.find(a => a.attempt_id === attemptId);
  if (attempt && attempt.quiz_id) {
    router.push(`/user/quiz-result/${attempt.quiz_id}`);
  }
};

// Load data on component mount
onMounted(() => {
  loadQuizHistory();
});
</script>

<style scoped>
.score-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.score-header {
  text-align: center;
  margin-bottom: 30px;
}

.score-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.5rem;
}

.score-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.search-section {
  margin-bottom: 30px;
}

.search-container {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 12px 45px 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #95a5a6;
  font-size: 1.1rem;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px 20px;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.retry-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #2980b9;
}

.results-section {
  margin-top: 20px;
}

.results-summary {
  text-align: center;
  margin-bottom: 20px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
}

.no-results-content {
  max-width: 400px;
  margin: 0 auto;
}

.no-results-content i {
  font-size: 4rem;
  color: #bdc3c7;
  margin-bottom: 20px;
}

.no-results-content h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.no-results-content p {
  color: #7f8c8d;
  line-height: 1.5;
}
</style> 