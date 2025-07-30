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
      <div 
        v-else-if="effectiveQuizState === 'upcoming'"
        class="countdown-timer"
      >
        <div class="countdown-label">Starts in:</div>
        <div class="countdown-display">
          <div v-if="countdown.days > 0" class="time-unit">
            <span class="time-value">{{ countdown.days }}</span>
            <span class="time-label">{{ countdown.days === 1 ? 'day' : 'days' }}</span>
          </div>
          <div v-if="countdown.hours > 0" class="time-unit">
            <span class="time-value">{{ countdown.hours }}</span>
            <span class="time-label">{{ countdown.hours === 1 ? 'hour' : 'hours' }}</span>
          </div>
          <div v-if="countdown.minutes > 0" class="time-unit">
            <span class="time-value">{{ countdown.minutes }}</span>
            <span class="time-label">{{ countdown.minutes === 1 ? 'min' : 'mins' }}</span>
          </div>
          <div v-if="countdown.seconds > 0 || (countdown.days === 0 && countdown.hours === 0 && countdown.minutes === 0)" class="time-unit">
            <span class="time-value">{{ countdown.seconds }}</span>
            <span class="time-label">{{ countdown.seconds === 1 ? 'sec' : 'secs' }}</span>
          </div>
        </div>
      </div>
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
import { computed, ref, onMounted, onUnmounted } from 'vue';
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

// Countdown logic
const countdown = ref({
  days: 0,
  hours: 0,
  minutes: 0,
  seconds: 0
});

let countdownInterval = null;

const updateCountdown = () => {
  const now = new Date();
  const quizDate = new Date(props.quiz.date);
  const timeDiff = quizDate.getTime() - now.getTime();

  if (timeDiff <= 0) {
    countdown.value = { days: 0, hours: 0, minutes: 0, seconds: 0 };
    return;
  }

  const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

  countdown.value = { days, hours, minutes, seconds };
};

onMounted(() => {
  updateCountdown();
  // Update every second
  countdownInterval = setInterval(updateCountdown, 1000);
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
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

.countdown-timer {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.countdown-timer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 20px;
}

.countdown-timer:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

.countdown-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  z-index: 1;
}

.countdown-display {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.time-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 0.5rem 0.75rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 45px;
}

.time-unit:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.time-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #2d3748;
  font-family: 'Arial', sans-serif;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.time-label {
  font-size: 0.625rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.25rem;
  line-height: 1;
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

  .countdown-timer {
    align-self: flex-end;
    padding: 0.75rem;
  }

  .time-unit {
    min-width: 40px;
    padding: 0.4rem 0.6rem;
  }

  .time-value {
    font-size: 1.1rem;
  }

  .time-label {
    font-size: 0.55rem;
  }
}
</style> 