<template>
  <div class="quiz-title-section">
    <div class="quiz-info">
      <h1>{{ quizDetails.quiz_title }}</h1>
      <div class="quiz-meta">
        <span>{{ quizDetails.subject_name }} > {{ quizDetails.chapter_name }}</span>
      </div>
    </div>
    <div class="quiz-timer" :class="{ 'warning': timeRemaining.hours < 1 }">
      <div class="timer-label">Time Remaining:</div>
      <div class="timer-value">
        {{ timeRemaining.hours }}h {{ timeRemaining.minutes }}m {{ timeRemaining.seconds }}s
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  quizDetails: {
    type: Object,
    required: true
  }
});

const timeRemaining = ref({ hours: 0, minutes: 0, seconds: 0 });
let timerInterval;

const calculateTimeRemaining = () => {
  const quizDate = new Date(props.quizDetails.quiz_date);
  const endTime = new Date(quizDate.getTime() + props.quizDetails.time_duration * 60000); // Convert minutes to milliseconds
  const now = new Date();
  
  const diff = endTime - now;
  
  if (diff <= 0) {
    // Quiz has ended
    timeRemaining.value = { hours: 0, minutes: 0, seconds: 0 };
    clearInterval(timerInterval);
    return;
  }

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  timeRemaining.value = { hours, minutes, seconds };
};

onMounted(() => {
  calculateTimeRemaining();
  timerInterval = setInterval(calculateTimeRemaining, 1000);
});

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});
</script>

<style scoped>
.quiz-title-section {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.quiz-title-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.quiz-info {
  flex: 1;
}

.quiz-info h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.quiz-meta {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.quiz-timer {
  text-align: right;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.quiz-timer:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.timer-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.timer-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  transition: color 0.3s ease;
}

.quiz-timer.warning .timer-value {
  color: #dc3545;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .quiz-title-section {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
    padding: 1.5rem;
  }
  
  .quiz-info h1 {
    font-size: 1.5rem;
  }
  
  .quiz-timer {
    text-align: center;
    padding: 0.75rem 1rem;
  }
  
  .timer-value {
    font-size: 1.25rem;
  }
}
</style> 