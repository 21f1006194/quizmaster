<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import QuestionFormModal from '@/components/modals/QuestionFormModal.vue';
import QuizFormModal from '@/components/modals/QuizFormModal.vue';

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const questions = ref([]);
const quizDetails = ref(null);
const loadingQuestions = ref(false);
const showQuestionModal = ref(false);
const editingQuestion = ref(null);
const showQuizModal = ref(false);

const fetchQuestions = async () => {
  try {
    loadingQuestions.value = true;
    const quizId = route.params.quizId;
    const response = await api.get(`/admin/api/quiz/${quizId}/questions`);
    questions.value = response.data.questions;
    quizDetails.value = response.data.quiz_details;
  } catch (error) {
    console.error('Error fetching questions:', error);
  } finally {
    loadingQuestions.value = false;
  }
};

const addQuestion = () => {
  showQuestionModal.value = true;
};

const handleQuestionAdded = async () => {
  await fetchQuestions();
};

const deleteQuestion = async (questionId) => {
  if (!confirm('Are you sure you want to delete this question?')) {
    return;
  }

  try {
    await api.delete(`/admin/api/questions/${questionId}`);
    await fetchQuestions();
  } catch (error) {
    console.error('Error deleting question:', error);
    alert('Failed to delete question');
  }
};

const handleEditClick = (question) => {
  editingQuestion.value = question;
  showQuestionModal.value = true;
};

const handleQuestionUpdated = async () => {
  await fetchQuestions();
  editingQuestion.value = null;
};

const deleteQuiz = async () => {
  if (!confirm('Are you sure you want to delete this quiz? This action cannot be undone.')) {
    return;
  }

  try {
    await api.delete(`/admin/api/quiz/${route.params.quizId}`);
    // Redirect to quiz list page
    router.push('/admin/quizzes');
  } catch (error) {
    console.error('Error deleting quiz:', error);
    alert('Failed to delete quiz');
  }
};

const handleQuizUpdated = async () => {
  await fetchQuestions();
};

onMounted(() => {
  fetchQuestions();
});
</script>

<template>
    <div class="container">
      <div v-if="quizDetails" class="selected-quiz">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>{{ quizDetails.quiz_title }}</h2>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-primary" @click="showQuizModal = true">
              <i class="bi bi-pencil-square"></i>
            </button>
            <button class="btn btn-outline-danger" @click="deleteQuiz">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>

        <div class="quiz-details mb-4">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Subject:</strong> {{ quizDetails.subject_name }}</p>
              <p><strong>Chapter:</strong> {{ quizDetails.chapter_name }}</p>
              <p><strong>Date:</strong> {{ quizDetails.quiz_date }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Duration:</strong> {{ quizDetails.time_duration }} minutes</p>
              <p><strong>Total Questions:</strong> {{ questions.length }}</p>
              <p><strong>Total Marks:</strong> {{ questions.reduce((sum, q) => sum + q.max_marks, 0) }}</p>
            </div>
          </div>
          <p v-if="quizDetails.remarks"><strong>Remarks:</strong> {{ quizDetails.remarks }}</p>
        </div>

        <!-- Questions List -->
        <div class="questions-container mb-4">
          <div v-if="loadingQuestions" class="text-center py-3">
            Loading questions...
          </div>
          
          <div v-else-if="questions.length === 0" class="text-center py-3">
            No questions added yet.
          </div>
          
          <div v-else class="questions-list">
            <div v-for="(question, index) in questions" 
                 :key="question.id" 
                 class="question-item">
              <div class="question-header d-flex justify-content-between align-items-center">
                <h5>Q{{ index + 1 }}. {{ question.question }}</h5>
                <div class="d-flex align-items-center gap-3">
                  <span class="badge bg-primary">{{ question.max_marks }} marks</span>
                  <button 
                    class="btn btn-link text-primary p-0" 
                    @click.stop="handleEditClick(question)"
                    title="Edit question"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button 
                    class="btn btn-link text-danger p-0" 
                    @click.stop="deleteQuestion(question.id)"
                    title="Delete question"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
              
              <div class="options-list mt-2">
                <div v-for="option in question.options" 
                     :key="option.id"
                     :class="['option-item', { 'correct-option': option.is_correct }]">
                  {{ option.option_text }}
                </div>
              </div>
              
              <hr v-if="index < questions.length - 1" class="my-4">
            </div>
          </div>
        </div>

        <button class="btn btn-primary" @click="addQuestion">
          <i class="bi bi-plus-circle me-2"></i>Add Question
        </button>
      </div>
      <div v-else class="no-quiz-selected">
        Loading quiz details...
      </div>
  </div>

  <QuizFormModal
    :show="showQuizModal"
    :quiz-details="quizDetails"
    @close="showQuizModal = false"
    @quiz-updated="handleQuizUpdated"
  />

  <QuestionFormModal
    :show="showQuestionModal"
    :quiz-id="route.params.quizId"
    :question="editingQuestion"
    :is-editing="!!editingQuestion"
    @close="showQuestionModal = false; editingQuestion = null;"
    @question-added="handleQuestionAdded"
    @question-updated="handleQuestionUpdated"
  />
</template>

<style scoped>
.admin-quiz-container {
  display: flex;
  height: calc(100vh - 80px);
  gap: 20px;
}

.chapter-title {
  margin-top: 15px;
  padding: 8px 0;
  border-bottom: 1px solid #dee2e6;
  color: #495057;
}

.quiz-item {
  padding: 8px 12px;
  margin: 4px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.quiz-item:hover {
  background-color: #e9ecef;
}

.quiz-item.active {
  background-color: #0d6efd;
  color: white;
}

.no-quiz-selected {
  text-align: center;
  color: #6c757d;
  margin-top: 40px;
}

.no-quizzes {
  padding: 8px 12px;
  color: #6c757d;
  font-style: italic;
}

.questions-container {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.question-item {
  padding: 10px 0;
}

.question-header {
  margin-bottom: 10px;
}

.question-header h5 {
  margin: 0;
  font-size: 1.1rem;
}

.options-list {
  padding-left: 20px;
}

.option-item {
  padding: 8px 12px;
  margin: 4px 0;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.correct-option {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #28a745;
}

hr {
  border-top: 1px solid #dee2e6;
}

.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}

.btn-link {
  text-decoration: none;
}

.btn-link:hover {
  opacity: 0.8;
}

.question-header .bi-pencil-square,
.question-header .bi-trash {
  font-size: 1.1rem;
}

.quiz-details {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.quiz-details p {
  margin-bottom: 0.5rem;
}
</style>