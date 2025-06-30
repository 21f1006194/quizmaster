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
    <button 
      v-if="isAdmin" 
      class="action-btn edit"
      @click="$emit('edit-quiz', quiz.id)"
    >
      Edit Quiz
    </button>

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
      <button 
        v-else
        class="action-btn results"
        @click="$emit('view-results', quiz.id)"
      >
        See Results
      </button>
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

const isAdmin = computed(() => authStore.user?.role === 'admin');

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
</script>

<style scoped>
.quiz-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.quiz-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.quiz-time {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
}

.quiz-details h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 5px;
}

.quiz-details p {
  font-size: 14px;
  color: #666;
}

.quiz-metadata {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}

.quiz-remarks {
  font-size: 13px;
  color: #666;
  font-style: italic;
  margin-top: 4px;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.action-btn.start {
  background-color: #28a745;
  color: white;
}

.action-btn.reminder {
  background-color: #6c757d;
  color: white;
}

.action-btn.results {
  background-color: #007bff;
  color: white;
}

.action-btn.edit {
  background-color: #ffc107;
  color: black;
}

@media (max-width: 768px) {
  .quiz-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .action-btn {
    align-self: flex-end;
  }
}
</style> 