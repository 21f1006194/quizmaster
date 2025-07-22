<template>
  <div class="quiz-result-container">
    <div v-if="loading" class="loading">Loading quiz results...</div>
    
    <div v-else-if="error" class="error-message">
      <div class="alert alert-danger">
        {{ error }}
      </div>
    </div>

    <div v-else class="result-content">
      <!-- Quiz Header with Results Summary -->
      <div class="result-header">
        <div class="quiz-info">
          <h1>{{ quizDetails?.quiz_title || 'Quiz Result' }}</h1>
          <div class="quiz-meta" v-if="quizDetails">
            <span>{{ quizDetails.subject_name }} > {{ quizDetails.chapter_name }}</span>
            <span class="quiz-date">Completed on: {{ formatDate(resultData?.end_time) }}</span>
          </div>
        </div>
        
        <div class="score-summary">
          <div class="score-card">
            <div class="score-title">Your Score</div>
            <div class="score-value">{{ resultData?.score || 0 }} / {{ totalMarks }}</div>
            <div class="score-percentage">{{ scorePercentage }}%</div>
          </div>
          
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Correct</div>
              <div class="stat-value correct">{{ correctAnswers }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Incorrect</div>
              <div class="stat-value incorrect">{{ incorrectAnswers }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Unanswered</div>
              <div class="stat-value unanswered">{{ unansweredQuestions }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Time Taken</div>
              <div class="stat-value">{{ formatDuration(timeTaken) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Questions and Answers Review -->
      <div class="questions-review">
        <h3>Questions Review</h3>
        
        <div v-for="(question, index) in questions" 
             :key="question.question_id" 
             class="question-review-item">
          
          <div class="question-header">
            <div class="question-number">Question {{ index + 1 }}</div>
            <div class="question-score">
              <span :class="getQuestionScoreClass(question)">
                {{ getQuestionScore(question) }} / {{ question.max_marks }} marks
              </span>
            </div>
          </div>

          <div class="question-content">
            <div class="question-text" v-html="question.question"></div>
            
            <div class="options-review">
              <div v-for="option in question.options" 
                   :key="option.option_id"
                   :class="getOptionClass(option)">
                <div class="option-content">
                  <div class="option-text">{{ option.option_text }}</div>
                  <div class="option-indicators">
                    <span v-if="option.is_selected" class="indicator user-selected">
                      Your Answer
                    </span>
                    <span v-if="option.is_correct" class="indicator correct-answer">
                      Correct Answer
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="!question.is_attempted" class="no-answer-message">
              <i class="bi bi-exclamation-triangle"></i>
              You did not answer this question
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="btn btn-primary" @click="goToDashboard">
          <i class="bi bi-house-door"></i> Back to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const props = defineProps({
  quizId: {
    type: String,
    required: true
  }
});

const router = useRouter();
const loading = ref(true);
const error = ref('');
const resultData = ref(null);
const questions = ref([]);
const quizDetails = ref(null);

// Computed properties for statistics
const totalMarks = computed(() => {
  return questions.value.reduce((sum, question) => sum + question.max_marks, 0);
});

const scorePercentage = computed(() => {
  if (totalMarks.value === 0) return 0;
  return Math.round((resultData.value?.score || 0) / totalMarks.value * 100);
});

const correctAnswers = computed(() => {
  return questions.value.filter(question => {
    if (!question.is_attempted) return false;
    // Check if any selected option is correct
    return question.options.some(option => 
      option.is_selected && option.is_correct
    );
  }).length;
});

const incorrectAnswers = computed(() => {
  return questions.value.filter(question => {
    if (!question.is_attempted) return false;
    // Check if is_selected is true and is_correct is false
    return question.options.some(option => 
      option.is_selected && !option.is_correct
    );
  }).length;
});

const unansweredQuestions = computed(() => {
  return questions.value.filter(question => !question.is_attempted).length;
});

const timeTaken = computed(() => {
  if (!resultData.value?.start_time || !resultData.value?.end_time) return null;
  const start = new Date(resultData.value.start_time);
  const end = new Date(resultData.value.end_time);
  return Math.floor((end - start) / 1000); // Return seconds
});

// Methods
const fetchQuizResult = async () => {
  try {
    loading.value = true;
    
    // Single API call to get complete quiz result
    const response = await api.get(`/user/api/quiz/${props.quizId}/result`);
    resultData.value = response.data;
    console.log(resultData.value);
    questions.value = response.data.responses || [];

    // Optional: Get quiz details for header (if available)
    try {
      const quizDetailsResponse = await api.get(`/user/api/quiz/${props.quizId}/questions`);
      quizDetails.value = quizDetailsResponse.data.quiz_details;
    } catch (detailsError) {
      console.warn('Could not fetch quiz details for header:', detailsError);
      // Continue without quiz details in header
    }

  } catch (err) {
    console.error('Error fetching quiz result:', err);
    if (err.response?.status === 400) {
      error.value = err.response.data.msg || 'No quiz result found. Please complete the quiz first.';
    } else {
      error.value = 'Failed to load quiz results. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};

const getOptionClass = (option) => {
  const classes = ['option-item'];
  
  if (option.is_selected) {
    classes.push('user-selected');
    if (option.is_correct) {
      classes.push('correct');
    } else {
      classes.push('incorrect');
    }
  } else if (option.is_correct) {
    classes.push('correct-answer');
  }
  
  return classes;
};

const getQuestionScore = (question) => {
  if (!question.is_attempted) return 0;
  
  // Check if the user selected the correct option
  let correct_answered_count = 0, total_correct_count = 0;
  question.options.forEach(option => {
    if (option.is_selected && option.is_correct) {
      correct_answered_count++;
    }
    if (option.is_correct) {
      total_correct_count++;
    }
  });
  return correct_answered_count * (question.max_marks / total_correct_count);
};

const getQuestionScoreClass = (question) => {
  const score = getQuestionScore(question);
  if (score === question.max_marks) return 'score-correct';
  if (score === 0 && question.is_attempted) return 'score-incorrect';
  return 'score-unanswered';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatDuration = (duration) => {
  if (!duration) return 'N/A';
  const minutes = Math.floor(duration / 60);
  const seconds = duration % 60;
  return `${minutes}m ${seconds}s`;
};

const goToDashboard = () => {
  router.push('/user/dashboard');
};

const reviewAgain = () => {
  // Scroll to top to review again
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  fetchQuizResult();
});
</script>

<style scoped>
.quiz-result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error-message {
  text-align: center;
  padding: 40px 20px;
  font-size: 18px;
}

.result-header {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.quiz-info h1 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.quiz-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: #7f8c8d;
  font-size: 14px;
}

.quiz-date {
  font-weight: 500;
}

.score-summary {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-top: 20px;
}

.score-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  min-width: 180px;
}

.score-title {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 5px;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.score-percentage {
  font-size: 18px;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  flex: 1;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-label {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 5px;
  text-transform: uppercase;
  font-weight: 500;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
}

.stat-value.correct { color: #28a745; }
.stat-value.incorrect { color: #dc3545; }
.stat-value.unanswered { color: #ffc107; }

.questions-review {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.questions-review h3 {
  margin: 0 0 25px 0;
  color: #2c3e50;
  border-bottom: 2px solid #ecf0f1;
  padding-bottom: 10px;
}

.question-review-item {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid #ecf0f1;
}

.question-review-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-number {
  font-weight: bold;
  color: #2c3e50;
  font-size: 16px;
}

.question-score {
  margin-left: auto;
}

.score-correct { color: #28a745; font-weight: bold; }
.score-incorrect { color: #dc3545; font-weight: bold; }
.score-unanswered { color: #ffc107; font-weight: bold; }

.question-text {
  font-size: 16px;
  margin-bottom: 20px;
  line-height: 1.6;
  color: #2c3e50;
}

.options-review {
  margin-left: 20px;
}

.option-item {
  margin: 10px 0;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid transparent;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.option-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option-text {
  flex: 1;
}

.option-indicators {
  display: flex;
  gap: 10px;
}

.indicator {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.user-selected {
  background: #007bff;
  color: white;
}

.correct-answer {
  background: #28a745;
  color: white;
}

.option-item.user-selected.correct {
  background: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.option-item.user-selected.incorrect {
  background: #f8d7da;
  border-color: #dc3545;
  color: #721c24;
}

.option-item.correct-answer {
  background: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.no-answer-message {
  margin: 15px 0;
  padding: 12px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  color: #856404;
  font-style: italic;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  padding: 20px 0;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 2px solid #6c757d;
}

.btn-outline-secondary:hover {
  background: #6c757d;
  color: white;
}

@media (max-width: 768px) {
  .score-summary {
    flex-direction: column;
    gap: 20px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .option-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>