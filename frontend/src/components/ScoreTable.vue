<template>
  <div class="score-table">
    <div class="score-cards">
      <div 
        v-for="attempt in quizHistory" 
        :key="attempt.attempt_id"
        class="score-card"
      >
        <!-- Quiz Info Section -->
        <div class="quiz-info">
          <div class="quiz-header">
            <div class="quiz-title-section">
              <h3 class="quiz-title">{{ attempt.quiz_title }}</h3>
              <div class="quiz-meta-inline">
                <span class="meta-inline-item">
                  <i class="bi bi-book"></i>
                  {{ attempt.subject_name }}
                </span>
                <span class="meta-inline-item">
                  <i class="bi bi-collection"></i>
                  {{ attempt.chapter_name }}
                </span>
                <span class="meta-inline-item">
                  <i class="bi bi-calendar-event"></i>
                  {{ formatDate(attempt.quiz_date) }}
                </span>
              </div>
            </div>
            <div class="quiz-badge" :class="getScoreBadgeClass(attempt.score, attempt.max_marks)">
              {{ getScorePercentage(attempt.score, attempt.max_marks) }}%
            </div>
          </div>
        </div>

        <!-- Quiz Stats -->
        <div class="quiz-stats">
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Total Questions:</span>
              <span class="stat-value">{{ attempt.total_questions }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Max Marks:</span>
              <span class="stat-value">{{ attempt.max_marks }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Duration:</span>
              <span class="stat-value">{{ formatDuration(attempt.time_duration) }}</span>
            </div>
          </div>
        </div>

        <!-- Attempt Details -->
        <div class="attempt-details">
          <div class="attempt-header">
            <h4>Your Performance</h4>
            <div class="score-display">
              <span class="score">{{ attempt.score }}</span>
              <span class="score-separator">/</span>
              <span class="max-score">{{ attempt.max_marks }}</span>
            </div>
          </div>

          <div class="performance-stats">
            <div class="performance-item correct">
              <i class="bi bi-check-circle"></i>
              <span class="performance-label">Correct:</span>
              <span class="performance-value">{{ attempt.correct_count }}</span>
            </div>
            <div class="performance-item incorrect">
              <i class="bi bi-x-circle"></i>
              <span class="performance-label">Incorrect:</span>
              <span class="performance-value">{{ attempt.wrong_count }}</span>
            </div>
            <div class="performance-item unattempted">
              <i class="bi bi-dash-circle"></i>
              <span class="performance-label">Unattempted:</span>
              <span class="performance-value">{{ attempt.unattempted_count }}</span>
            </div>
          </div>

          <div class="attempt-timing">
            <div class="timing-item">
              <i class="bi bi-play-circle"></i>
              <span>Started: {{ formatDateTime(attempt.start_time) }}</span>
            </div>
            <button 
              @click="$emit('view-result', attempt.attempt_id)"
              class="view-result-btn"
            >
              <i class="bi bi-eye"></i>
              View Result
            </button>
            <div class="timing-item">
              <i class="bi bi-stop-circle"></i>
              <span>Completed: {{ formatDateTime(attempt.end_time) }}</span>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

// Props
const props = defineProps({
  quizHistory: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Emits
const emit = defineEmits(['view-result']);

// Helper functions
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatDuration = (minutes) => {
  if (!minutes) return 'N/A';
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
};

const getScorePercentage = (score, maxMarks) => {
  if (!maxMarks || maxMarks === 0) return 0;
  return Math.round((score / maxMarks) * 100);
};

const getScoreBadgeClass = (score, maxMarks) => {
  const percentage = getScorePercentage(score, maxMarks);
  
  if (percentage >= 90) return 'excellent';
  if (percentage >= 80) return 'good';
  if (percentage >= 70) return 'average';
  if (percentage >= 60) return 'below-average';
  return 'poor';
};
</script>

<style scoped>
.score-table {
  width: 100%;
}

.score-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 10px 0;
}

.score-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #e1e8ed;
}

.score-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.quiz-info {
  margin-bottom: 12px;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.quiz-title-section {
  flex: 1;
  margin-right: 12px;
}

.quiz-title {
  margin: 0 0 4px 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.2;
}

.quiz-meta-inline {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.meta-inline-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #7f8c8d;
  font-size: 0.8rem;
}

.meta-inline-item i {
  color: #95a5a6;
  font-size: 0.75rem;
}

.quiz-badge {
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.quiz-badge.excellent {
  background-color: #d4edda;
  color: #155724;
}

.quiz-badge.good {
  background-color: #d1ecf1;
  color: #0c5460;
}

.quiz-badge.average {
  background-color: #fff3cd;
  color: #856404;
}

.quiz-badge.below-average {
  background-color: #f8d7da;
  color: #721c24;
}

.quiz-badge.poor {
  background-color: #f5c6cb;
  color: #721c24;
}



.quiz-stats {
  margin-bottom: 12px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.stats-grid {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: #6c757d;
  font-weight: 500;
}

.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.attempt-details {
  margin-bottom: 12px;
}

.attempt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e9ecef;
}

.attempt-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 5px;
}

.score {
  font-size: 1.1rem;
  font-weight: 700;
  color: #3498db;
}

.score-separator {
  color: #6c757d;
  font-weight: 500;
}

.max-score {
  font-size: 1rem;
  color: #6c757d;
  font-weight: 500;
}

.performance-stats {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.performance-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 6px;
  flex: 1;
}

.performance-item.correct {
  background-color: #d4edda;
  color: #155724;
}

.performance-item.incorrect {
  background-color: #f8d7da;
  color: #721c24;
}

.performance-item.unattempted {
  background-color: #e2e3e5;
  color: #383d41;
}

.performance-item i {
  font-size: 0.9rem;
}

.performance-label {
  font-size: 0.75rem;
  font-weight: 500;
}

.performance-value {
  font-size: 1rem;
  font-weight: 700;
}

.attempt-timing {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.timing-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #6c757d;
}

.timing-item i {
  color: #95a5a6;
  width: 16px;
}



.view-result-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.view-result-btn:hover {
  background-color: #2980b9;
}

.view-result-btn:active {
  transform: translateY(1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .quiz-meta-inline {
    flex-direction: column;
    gap: 6px;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .quiz-title-section {
    margin-right: 0;
  }
  
  .stats-grid {
    flex-direction: column;
    gap: 6px;
  }
  
  .performance-stats {
    flex-direction: column;
    gap: 6px;
  }
  
  .attempt-timing {
    flex-direction: column;
    gap: 8px;
  }
  
  .attempt-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style> 