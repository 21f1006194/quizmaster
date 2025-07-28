<template>
  <div class="question-section">
    <div class="question-header">
      <h2>Question {{ currentIndex + 1 }} of {{ questions.length }}</h2>
    </div>
    
    <div class="question-content">
      <h3 v-html="currentQuestion?.question"></h3>
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
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.question-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.question-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
}

.question-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.options {
  margin: 2rem 0;
}

.option {
  margin: 1rem 0;
  padding: 1rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.option:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.option input[type="radio"] {
  margin-right: 0.75rem;
  transform: scale(1.2);
  accent-color: #667eea;
}

.option label {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  line-height: 1.5;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
}

.right-buttons {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  min-width: 60%;
}

.nav-btn {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.nav-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.nav-btn.primary {
  background: linear-gradient(45deg, #28a745 0%, #218838 100%);
  color: white;
}

.nav-btn.review {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.nav-btn.review.active {
  background: linear-gradient(45deg, #495057 0%, #343a40 100%);
  border: 2px solid #212529;
  box-shadow: 0 6px 20px rgba(73, 80, 87, 0.3);
}

.nav-btn.clear {
  background: linear-gradient(45deg, #6c757d 0%, #5a6268 100%);
  color: white;
}

.nav-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #f8f9fa;
  color: #6c757d;
  box-shadow: none;
}

.nav-btn.primary:disabled {
  background: #e9ecef;
  color: #6c757d;
}

.nav-btn.review:disabled {
  background: #e9ecef;
  color: #6c757d;
}

.nav-btn.icon-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #333;
  border: 1px solid #e0e0e0;
}

.nav-btn.icon-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  transform: scale(1.05);
}

.nav-btn.icon-btn:disabled {
  background: #f8f9fa;
  color: #adb5bd;
  border-color: #e9ecef;
}

.finish-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #f0f0f0;
  text-align: center;
}

.nav-btn.finish {
  background: linear-gradient(45deg, #dc3545 0%, #c82333 100%);
  color: white;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 700;
}

@media (max-width: 768px) {
  .question-section {
    padding: 1.5rem;
  }
  
  .right-buttons {
    min-width: 100%;
    justify-content: center;
    margin-top: 1rem;
  }
  
  .navigation-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.8rem;
  }
  
  .nav-btn.icon-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style> 