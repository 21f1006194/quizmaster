<template>
  <div class="question-section">
    <div class="question-header">
      <h2>Question {{ currentIndex + 1 }} of {{ questions.length }}</h2>
    </div>
    
    <div class="question-content">
      <h3>{{ currentQuestion?.question }}</h3>
      <div class="options">
        <div v-for="option in currentQuestion?.options" :key="option.id" class="option">
          <input 
            type="radio" 
            :id="option.id" 
            :value="option.id"
            v-model="currentQuestion.selected_option"
            name="answer"
          >
          <label :for="option.id">{{ option.option_text }}</label>
        </div>
      </div>
    </div>

    <div class="navigation-buttons">
      <button 
        @click="previousQuestion" 
        :disabled="currentIndex === 0"
        class="nav-btn icon-btn"
        title="Previous"
      >
        &#10094;
      </button>
      <div class="right-buttons">
        <button 
          v-if="currentQuestion?.selected_option"
          @click="clearResponse" 
          class="nav-btn clear"
        >
          Clear Response
        </button>
        <button 
          @click="markForReviewLater" 
          class="nav-btn review"
          :class="{ active: currentQuestion?.status === 'review-later' }"
          :disabled="currentQuestion?.selected_option"
        >
          Review Later
        </button>
        <button 
          @click="saveAndReview" 
          class="nav-btn review"
          :disabled="!currentQuestion?.selected_option"
        >
          Save & Review
        </button>
        <button 
          @click="saveAndNext" 
          class="nav-btn primary"
          :disabled="!currentQuestion?.selected_option"
        >
          Save & Next
        </button>
        <button 
          @click="nextQuestion"
          class="nav-btn icon-btn"
          title="Next"
        >
          &#10095;
        </button>
      </div>
    </div>

    <div class="finish-section" v-if="currentIndex === questions.length - 1">
      <button 
        @click="finishQuiz" 
        class="nav-btn finish"
      >
        Finish Quiz
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const props = defineProps({
  questions: {
    type: Array,
    required: true
  },
  quizId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['question-changed', 'quiz-finished']);

const router = useRouter();
const currentIndex = ref(0);

const currentQuestion = computed(() => {
  return props.questions[currentIndex.value] || null;
});

const clearResponse = async () => {
  if (!currentQuestion.value) return;

  try {
    await api.post(`/user/api/quiz/${props.quizId}/attempt`, {
      question_id: currentQuestion.value.id,
      selected_option_id: null
    });
    currentQuestion.value.selected_option = null;
    currentQuestion.value.status = 'visited';
    emit('question-changed', currentIndex.value);
  } catch (error) {
    console.error('Error clearing response:', error);
  }
};

const saveAnswer = async () => {
  if (!currentQuestion.value?.selected_option) return;

  try {
    await api.post(`/user/api/quiz/${props.quizId}/attempt`, {
      question_id: currentQuestion.value.id,
      selected_option_id: currentQuestion.value.selected_option
    });
    currentQuestion.value.status = 'answered';
    emit('question-changed', currentIndex.value);
  } catch (error) {
    console.error('Error saving answer:', error);
  }
};

const saveAndNext = async () => {
  await saveAnswer();
  nextQuestion();
};

const previousQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    if (currentQuestion.value.status === 'not-visited') {
      currentQuestion.value.status = 'visited';
      emit('question-changed', currentIndex.value);
    }
  }
};

const nextQuestion = () => {
  if (currentIndex.value < props.questions.length - 1) {
    currentIndex.value++;
    if (currentQuestion.value.status === 'not-visited') {
      currentQuestion.value.status = 'visited';
      emit('question-changed', currentIndex.value);
    }
  }
};

const markForReviewLater = () => {
  if (currentQuestion.value) {
    currentQuestion.value.status = 'review-later';
    emit('question-changed', currentIndex.value);
    nextQuestion();
  }
};

const saveAndReview = async () => {
  await saveAnswer();
  if (currentQuestion.value) {
    currentQuestion.value.status = 'save-review';
    emit('question-changed', currentIndex.value);
    nextQuestion();
  }
};

const finishQuiz = async () => {
  await saveAnswer();
  try {
    await api.put(`/user/api/quiz/${props.quizId}`, {
      stop_quiz: true
    });
    emit('quiz-finished');
  } catch (error) {
    console.error('Error finishing quiz:', error);
  }
};

// Method to jump to a specific question
const jumpToQuestion = (index) => {
  currentIndex.value = index;
  if (props.questions[index].status === 'not-visited') {
    props.questions[index].status = 'visited';
    emit('question-changed', index);
  }
};

// Expose methods to parent
defineExpose({
  jumpToQuestion,
  currentIndex
});
</script>

<style scoped>
.question-section {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.options {
  margin: 20px 0;
}

.option {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.right-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  min-width: 60%;
}

.nav-btn {
  padding: 8px 15px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.nav-btn.primary {
  background-color: #4CAF50;
  color: white;
}

.nav-btn.review {
  background-color: #2196F3;
  color: white;
}

.nav-btn.review.active {
  background-color: #1976D2;
  border: 2px solid #1565C0;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #ccc;
}

.nav-btn.primary:disabled {
  background-color: #88c98a;
}

.nav-btn.review:disabled {
  background-color: #90caf9;
}

.nav-btn.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background-color: #f5f5f5;
  color: #333;
  transition: all 0.2s;
}

.nav-btn.icon-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.nav-btn.icon-btn:disabled {
  background-color: #f5f5f5;
  color: #ccc;
}

.finish-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: center;
}

.nav-btn.finish {
  background-color: #ff5722;
  color: white;
  padding: 12px 30px;
  font-size: 16px;
}
</style> 