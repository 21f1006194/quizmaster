<template>
  <div class="quiz-container">
    <div v-if="loading" class="loading">Loading quiz...</div>
    
    <div v-else class="quiz-layout">
      <!-- Add QuizTitle component -->
      <QuizTitle :quiz-details="quizDetails" />
      
      <div class="quiz-content">
        <!-- Question Sidebar -->
        <div class="question-sidebar">
          <div class="sidebar-title">Questions</div>
          <QuestionDots
            :questions="questions"
            :current-index="currentIndex"
            @question-clicked="handleQuestionClick"
          />
        </div>

        <!-- Question Content -->
        <QuestionContent
          ref="questionContentRef"
          :questions="questions"
          :quiz-id="quizId"
          @question-changed="handleQuestionChange"
          @quiz-finished="handleQuizFinish"
        />
      </div>
    </div>
    <WarningModal
      v-if="showWarningModal"
      title="Couldn't Start Quiz"
      :message="errorMessage"
      :isVisible="showWarningModal"
      @close="handleModalClose"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import WarningModal from '@/components/modals/QuizErrorModal.vue';
import QuestionDots from '@/components/quiz/QuestionDots.vue';
import QuestionContent from '@/components/quiz/QuestionContent.vue';
import QuizTitle from '@/components/quiz/QuizTitle.vue';

const props = defineProps({
  quizId: {
    type: String,
    required: true
  }
});

const router = useRouter();
const questions = ref([]);
const loading = ref(true);
const showWarningModal = ref(false);
const errorMessage = ref('');
const questionContentRef = ref(null);
const currentIndex = ref(0);
const quizDetails = ref(null);

const fetchQuestionsAndResponses = async () => {
  try {
    // Fetch questions first
    const questionsResponse = await api.get(`/user/api/quiz/${props.quizId}/questions`);
    
    // Store quiz details
    quizDetails.value = questionsResponse.data.quiz_details;
    
    // Initialize questions with default state
    questions.value = questionsResponse.data.questions.map(q => ({
      ...q,
      status: 'not-visited',
      selected_option: null
    }));

    // Try to fetch existing responses
    try {
      const responsesResponse = await api.get(`/user/api/quiz/${props.quizId}/attempt`);
      
      // If we got responses, update the questions with saved answers
      if (responsesResponse.status === 200) {
        const responses = responsesResponse.data.responses;
        
        // Update questions with saved responses
        questions.value = questions.value.map(question => {
          const savedResponse = responses.find(r => r.question_id === question.id);
          if (savedResponse) {
            return {
              ...question,
              selected_option: savedResponse.option_id,
              status: savedResponse.is_attempted ? 'answered' : 'visited'
            };
          }
          return question;
        });
      }
    } catch (error) {
      // If 404, it means no active attempt, which is fine
      if (error.response?.status !== 404) {
        console.error('Error fetching responses:', error);
      }
    }

    loading.value = false;
  } catch (error) {
    console.error('Error fetching questions:', error);
    loading.value = false;
  }
};

const startQuizAttempt = async () => {
  try {
    const response = await api.post(`/user/api/quiz/${props.quizId}`, {
      start_quiz: true
    });
    console.log(response.data.msg);
  } catch (error) {
    // Show warning modal with error message
    errorMessage.value = error.response?.data?.msg || 'An unknown error occurred.';
    showWarningModal.value = true;
  }
};

const handleQuestionClick = (index) => {
  if (questionContentRef.value) {
    questionContentRef.value.jumpToQuestion(index);
  }
};

const handleQuestionChange = (index) => {
  currentIndex.value = index;
};

const handleQuizFinish = () => {
  router.push('/user/dashboard');
};

const handleModalClose = () => {
  showWarningModal.value = false;
  router.push('/user/dashboard');
};

onMounted(async () => {
  await startQuizAttempt();
  await fetchQuestionsAndResponses();
  if (questions.value.length > 0 && questions.value[0].status === 'not-visited') {
    questions.value[0].status = 'visited';
  }
});
</script>

<style scoped>
.quiz-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.quiz-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quiz-content {
  display: flex;
  gap: 20px;
}

.question-sidebar {
  width: 300px;
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  height: fit-content;
}

.sidebar-title {
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #666;
}
</style> 