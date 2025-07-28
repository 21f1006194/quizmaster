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
              Result
            </button>
            <button 
              @click="$emit('view-leaderboard', attempt.attempt_id)"
              class="view-leaderboard-btn"
            >
              <i class="bi bi-trophy"></i>
              Leaderboard
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
  gap: 1.5rem;
  padding: 1rem 0;
}

.score-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.score-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.quiz-info {
  margin-bottom: 1.5rem;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.quiz-title-section {
  flex: 1;
  margin-right: 1rem;
}

.quiz-title {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
}

.quiz-meta-inline {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-inline-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.875rem;
  font-weight: 500;
}

.meta-inline-item i {
  color: #95a5a6;
  font-size: 0.875rem;
}

.quiz-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.quiz-badge.excellent {
  background: linear-gradient(45deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid #c3e6cb;
}

.quiz-badge.good {
  background: linear-gradient(45deg, #d1ecf1 0%, #bee5eb 100%);
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.quiz-badge.average {
  background: linear-gradient(45deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.quiz-badge.below-average {
  background: linear-gradient(45deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.quiz-badge.poor {
  background: linear-gradient(45deg, #f5c6cb 0%, #f1b0b7 100%);
  color: #721c24;
  border: 1px solid #f1b0b7;
}

.quiz-stats {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  border: 1px solid #e0e0e0;
}

.stats-grid {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  font-weight: 600;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #333;
}

.attempt-details {
  margin-bottom: 1.5rem;
}

.attempt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.attempt-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.125rem;
  font-weight: 700;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.score {
  font-size: 1.25rem;
  font-weight: 700;
  color: #667eea;
}

.score-separator {
  color: #666;
  font-weight: 600;
}

.max-score {
  font-size: 1rem;
  color: #666;
  font-weight: 600;
}

.performance-stats {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.performance-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  flex: 1;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.performance-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.performance-item.correct {
  background: linear-gradient(45deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid #c3e6cb;
}

.performance-item.incorrect {
  background: linear-gradient(45deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.performance-item.unattempted {
  background: linear-gradient(45deg, #e2e3e5 0%, #d6d8db 100%);
  color: #383d41;
  border: 1px solid #d6d8db;
}

.performance-item i {
  font-size: 1rem;
}

.performance-label {
  font-size: 0.875rem;
  font-weight: 600;
}

.performance-value {
  font-size: 1.125rem;
  font-weight: 700;
}

.attempt-timing {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  border: 1px solid #e0e0e0;
}

.timing-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  font-weight: 500;
}

.timing-item i {
  color: #95a5a6;
  width: 1rem;
}

.view-result-btn {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.view-result-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.view-result-btn:active {
  transform: translateY(0);
}

.view-leaderboard-btn {
  background: linear-gradient(45deg, #ffc107 0%, #e0a800 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
}

.view-leaderboard-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
}

.view-leaderboard-btn:active {
  transform: translateY(0);
}

/* Responsive Design */
@media (max-width: 768px) {
  .score-card {
    padding: 1.5rem;
  }
  
  .quiz-meta-inline {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .quiz-title-section {
    margin-right: 0;
  }
  
  .stats-grid {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .performance-stats {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .attempt-timing {
    flex-direction: column;
    gap: 1rem;
  }
  
  .attempt-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style> 