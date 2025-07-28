<template>
  <div class="score-view">
    <div class="score-header">
      <h1>Quiz Results</h1>
      <p>View your quiz results history.</p>
    </div>

    <!-- Search Bar -->
    <div class="search-section">
      <div class="search-container" style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
        <div style="flex: 1; position: relative;">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by subject, chapter, or quiz title..."
            class="search-input"
            @input="filterResults"
          />
          <i class="bi bi-search search-icon"></i>
        </div>
        <div style="position: relative;">
          <button
            class="download-btn"
            :disabled="downloadDisabled"
            @click="downloadCSV"
          >
            <i class="bi bi-download"></i> Download Full CSV
          </button>
          <transition name="fade">
            <div v-if="showDownloadMsg" class="download-popup">
              {{ downloadMsg }}
            </div>
          </transition>
        </div>
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
          @view-leaderboard="viewLeaderboard"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import ScoreTable from '@/components/ScoreTable.vue';

const router = useRouter();

// Data refs
const quizHistory = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');

// Download CSV state
const showDownloadMsg = ref(false);
const downloadMsg = ref('');
const downloadDisabled = ref(false);
let downloadMsgTimeout = null;
let downloadBtnTimeout = null;
let currentEventSource = null;

const downloadCSV = async () => {
  if (downloadDisabled.value) return;
  downloadDisabled.value = true;
  showDownloadMsg.value = false;
  downloadMsg.value = 'Initializing download...';
  showDownloadMsg.value = true;

  // Close any existing EventSource connection
  if (currentEventSource) {
    currentEventSource.close();
  }
  
  let eventSource = null;
  
  try {
    // First, trigger the download process
    const response = await api.post('/user/api/quiz/history/download');
    downloadMsg.value = response.data.msg || 'CSV download triggered';
    
    // Create EventSource to listen for SSE events
    const baseURL = import.meta.env.VITE_BASE_URL || '';
    const token = localStorage.getItem('token');
    const streamUrl = `${baseURL}/stream`;
    
    eventSource = new EventSource(streamUrl);
    currentEventSource = eventSource;
    
    eventSource.onmessage = async (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.download_url) {
          downloadMsg.value = 'Downloading CSV file...';
          
          // Use the api instance to download the file
          const downloadResponse = await api.get(data.download_url, {
            responseType: 'blob'
          });
          
          // Create a download link and trigger download
          const blob = new Blob([downloadResponse.data], { 
            type: 'text/csv' 
          });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `quiz_history_${new Date().toISOString().split('T')[0]}.csv`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
          
          downloadMsg.value = 'CSV downloaded successfully!';
          
          // Close the EventSource connection
          eventSource.close();
          currentEventSource = null;
          
          // Re-enable button immediately after successful download
          downloadDisabled.value = false;
        }
      } catch (parseError) {
        console.error('Error parsing SSE message:', parseError);
        downloadMsg.value = 'Error processing download response';
        eventSource?.close();
        currentEventSource = null;
        downloadDisabled.value = false;
      }
    };
    
    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      downloadMsg.value = 'Connection error. Please try again.';
      eventSource?.close();
      currentEventSource = null;
      downloadDisabled.value = false;
    };
    
    // Set a timeout to close the connection if no response
    setTimeout(() => {
      if (eventSource && eventSource.readyState !== EventSource.CLOSED) {
        eventSource.close();
        currentEventSource = null;
        downloadMsg.value = 'Download timeout. Please try again.';
        downloadDisabled.value = false;
      }
    }, 30000); // 30 second timeout
    
  } catch (err) {
    downloadMsg.value = err.response?.data?.msg || 'Failed to trigger CSV download';
    eventSource?.close();
    currentEventSource = null;
    downloadDisabled.value = false;
  } finally {
    // Hide popup after 5s for success, 3s for error
    if (downloadMsgTimeout) clearTimeout(downloadMsgTimeout);
    const hideDelay = downloadMsg.value.includes('successfully') ? 5000 : 3000;
    downloadMsgTimeout = setTimeout(() => {
      showDownloadMsg.value = false;
    }, hideDelay);
  }
};

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

// Navigate to leaderboard view
const viewLeaderboard = (attemptId) => {
  const attempt = quizHistory.value.find(a => a.attempt_id === attemptId);
  if (attempt && attempt.quiz_id) {
    router.push(`/leaderboard/${attempt.quiz_id}`);
  }
};

// Load data on component mount
onMounted(() => {
  loadQuizHistory();
});

// Cleanup EventSource on component unmount
onUnmounted(() => {
  if (currentEventSource) {
    currentEventSource.close();
    currentEventSource = null;
  }
  if (downloadMsgTimeout) {
    clearTimeout(downloadMsgTimeout);
  }
  if (downloadBtnTimeout) {
    clearTimeout(downloadBtnTimeout);
  }
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
  margin-bottom: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.score-header:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.score-header h1 {
  color: #333;
  margin-bottom: 0.75rem;
  font-size: 2.5rem;
  font-weight: 700;
}

.score-header p {
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
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
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  margin: 1rem 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f0f0f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  font-size: 1.2rem;
  color: #666;
  font-weight: 500;
  margin: 0;
}

.error-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  margin: 1rem 0;
}

.alert {
  padding: 1.5rem;
  border-radius: 15px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.alert-danger {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 50px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.results-section {
  margin-top: 1.5rem;
}

.results-summary {
  text-align: center;
  margin-bottom: 20px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  margin: 1rem 0;
}

.no-results-content {
  max-width: 400px;
  margin: 0 auto;
}

.no-results-content i {
  font-size: 4rem;
  color: #667eea;
  margin-bottom: 1.5rem;
  opacity: 0.7;
}

.no-results-content h3 {
  color: #333;
  margin-bottom: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.no-results-content p {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
}

.download-btn {
  background: linear-gradient(45deg, #28a745 0%, #218838 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.download-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.download-btn:disabled {
  background: linear-gradient(45deg, #6c757d 0%, #5a6268 100%);
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
}

.download-popup {
  position: absolute;
  right: 0;
  top: 110%;
  background: #333;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 15px;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 10;
  opacity: 0.95;
  border: 1px solid #444;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .score-view {
    padding: 1.5rem;
  }
  
  .score-header {
    padding: 1.5rem;
  }
  
  .score-header h1 {
    font-size: 2rem;
  }
  
  .search-container {
    padding: 1.25rem;
  }
  
  .loading-state,
  .error-state,
  .no-results {
    padding: 3rem 1.5rem;
  }
  
  .search-input {
    padding: 0.875rem 2.5rem 0.875rem 1.25rem;
    font-size: 0.875rem;
  }
  
  .search-icon {
    right: 2rem;
    font-size: 1.1rem;
  }
}
</style> 