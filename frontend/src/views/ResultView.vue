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

.download-btn {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 7px;
  transition: background-color 0.3s ease, opacity 0.3s;
  box-shadow: 0 2px 8px rgba(39, 174, 96, 0.08);
}
.download-btn:disabled {
  background-color: #b2bec3;
  cursor: not-allowed;
  opacity: 0.7;
}
.download-popup {
  position: absolute;
  right: 0;
  top: 110%;
  background: #222;
  color: #fff;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 0.98rem;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.13);
  z-index: 10;
  opacity: 0.97;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 