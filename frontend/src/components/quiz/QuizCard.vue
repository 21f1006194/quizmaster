<template>
  <div class="quiz-item">
    <div class="quiz-info">
      <div class="quiz-time">
        <span class="icon">⏱️</span>
      </div>
      <div class="quiz-details">
        <h3>{{ quiz.title }}</h3>
        <p>{{ quiz.subject }} | {{ quiz.chapter }}</p>
        <p class="quiz-metadata">
          Duration: {{ quiz.duration }} minutes | 
          Start Time: {{ new Date(quiz.date).toLocaleString() }}
        </p>
        <p v-if="quiz.remarks" class="quiz-remarks">{{ quiz.remarks }}</p>
      </div>
    </div>

    <!-- Admin View -->
    <template v-if="isAdmin">
      <button 
        v-if="effectiveQuizState === 'ongoing'"
        class="action-btn view"
        @click="$emit('view-quiz', quiz.id)"
      >
        View Quiz
      </button>
      <button 
        v-else-if="effectiveQuizState === 'upcoming'"
        class="action-btn edit"
        @click="editQuiz"
      >
        Edit Quiz
      </button>
      <div v-else-if="effectiveQuizState === 'previous'" class="action-buttons">
        <button 
          class="action-btn leaderboard"
          @click="viewLeaderboard"
        >
          Leaderboard
        </button>
      </div>
    </template>

    <!-- User View -->
    <template v-else>
      <button 
        v-if="effectiveQuizState === 'ongoing'"
        class="action-btn start"
        @click="startQuiz"
      >
        Start Quiz
      </button>
      <button 
        v-else-if="effectiveQuizState === 'upcoming'"
        class="action-btn reminder"
        @click="$emit('reminder-set', quiz.id)"
      >
        Set Reminder
      </button>
      <div v-else class="action-buttons">
        <button 
          class="action-btn results"
          @click="viewQuizResult"
        >
          Results
        </button>
        <button 
          class="action-btn leaderboard"
          @click="viewLeaderboard"
        >
          Leaderboard
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const props = defineProps({
  quiz: {
    type: Object,
    required: true
  },
  quizState: {
    type: String,
    required: false,
    validator: (value) => !value || ['ongoing', 'upcoming', 'previous'].includes(value)
  }
});

defineEmits(['reminder-set', 'view-results', 'edit-quiz']);

const isAdmin = computed(() => authStore.role === 'admin');

// Calculate quiz state if not provided or invalid
const calculateQuizState = () => {
  const now = new Date();
  const quizDate = new Date(props.quiz.date);
  const endDate = new Date(quizDate.getTime() + props.quiz.duration * 60000);

  if (now >= quizDate && now <= endDate) return 'ongoing';
  if (now < quizDate) return 'upcoming';
  return 'previous';
};

// Use provided state if valid, otherwise calculate it
const effectiveQuizState = computed(() => {
  if (props.quizState && ['ongoing', 'upcoming', 'previous'].includes(props.quizState)) {
    return props.quizState;
  }
  return calculateQuizState();
});

const startQuiz = () => {
  router.push(`/user/attempt-quiz/${props.quiz.id}`);
};

const editQuiz = () => {
  router.push(`/admin/quiz-edit/${props.quiz.id}`);
};

const viewQuizResult = () => {
  router.push(`/user/quiz-result/${props.quiz.id}`);
};

const viewLeaderboard = () => {
  router.push(`/leaderboard/${props.quiz.id}`);
};
</script>

<style scoped>
.quiz-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: white;
  border-radius: 20px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.quiz-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.quiz-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.quiz-time {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.quiz-time:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.quiz-details h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.quiz-details p {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.quiz-metadata {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
  font-weight: 500;
}

.quiz-remarks {
  font-size: 0.875rem;
  color: #666;
  font-style: italic;
  margin-top: 0.5rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.action-btn.start {
  background: linear-gradient(45deg, #28a745 0%, #218838 100%);
  color: white;
}

.action-btn.reminder {
  background: linear-gradient(45deg, #6c757d 0%, #5a6268 100%);
  color: white;
}

.action-btn.results {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.edit {
  background: linear-gradient(45deg, #ffc107 0%, #e0a800 100%);
  color: #333;
}

.action-btn.leaderboard {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.view {
  background: linear-gradient(45deg, #17a2b8 0%, #138496 100%);
  color: white;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .quiz-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    padding: 1.25rem;
  }
  
  .quiz-time {
    width: 48px;
    height: 48px;
  }
  
  .action-btn {
    align-self: flex-end;
  }

  .action-buttons {
    align-self: flex-end;
  }
}
</style> 