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
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-info {
  flex: 1;
}

.quiz-info h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.quiz-meta {
  color: #666;
  font-size: 14px;
}

.quiz-timer {
  text-align: right;
  padding: 10px 20px;
  background: #f5f5f5;
  border-radius: 4px;
}

.timer-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.timer-value {
  font-size: 20px;
  font-weight: bold;
  color: #2196F3;
}

.quiz-timer.warning .timer-value {
  color: #ff5252;
}
</style> 