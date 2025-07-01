<template>
  <div class="question-dots-container">
    <div class="question-dots">
      <button
        v-for="(question, index) in questions"
        :key="question.id"
        class="question-dot"
        :class="{
          'answered': question.status === 'answered',
          'visited': question.status === 'visited',
          'review-later': question.status === 'review-later',
          'save-review': question.status === 'save-review',
          'current': currentIndex === index
        }"
        @click="$emit('question-clicked', index)"
      >
        {{ index + 1 }}
      </button>
    </div>
    <div class="legend">
      <div class="legend-item">
        <span class="dot answered"></span>
        <span>Answered</span>
      </div>
      <div class="legend-item">
        <span class="dot visited"></span>
        <span>Visited</span>
      </div>
      <div class="legend-item">
        <span class="dot review-later"></span>
        <span>Review Later</span>
      </div>
      <div class="legend-item">
        <span class="dot save-review"></span>
        <span>Save & Review</span>
      </div>
      <div class="legend-item">
        <span class="dot"></span>
        <span>Not Visited</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  questions: {
    type: Array,
    required: true
  },
  currentIndex: {
    type: Number,
    required: true
  }
});

defineEmits(['question-clicked']);
</script>

<style scoped>
.question-dots-container {
  width: 100%;
}

.question-dots {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 25px;
}

.question-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: white;
  font-size: 16px;
  transition: all 0.2s;
}

.question-dot.answered {
  background: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.question-dot.visited:not(.answered) {
  background: #ff5252;
  border-color: #ff5252;
  color: white;
}

.question-dot.current {
  border-color: #2196F3;
  border-width: 3px;
}

.question-dot.review-later {
  background: #2196F3;
  border-color: #2196F3;
  color: white;
}

.question-dot.save-review {
  background: #4CAF50;
  border-color: #2196F3;
  border-width: 3px;
  color: white;
}

.legend {
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
  border: 2px solid #ddd;
}

.dot.answered {
  background: #4CAF50;
  border-color: #4CAF50;
}

.dot.visited {
  background: #ff5252;
  border-color: #ff5252;
}

.dot.review-later {
  background: #2196F3;
  border-color: #2196F3;
}

.dot.save-review {
  background: #4CAF50;
  border-color: #2196F3;
  border-width: 3px;
}
</style> 