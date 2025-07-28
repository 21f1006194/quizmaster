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
    <div class="admin-quiz-edit-container">
      <div v-if="quizDetails" class="selected-quiz">
        <div class="quiz-header">
          <h2>{{ quizDetails.quiz_title }}</h2>
          <div class="quiz-actions">
            <button class="action-btn edit-btn" @click="showQuizModal = true">
              <i class="bi bi-pencil-square"></i>
            </button>
            <button class="action-btn delete-btn" @click="deleteQuiz">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>

        <div class="quiz-details">
          <div class="quiz-info-grid">
            <div class="quiz-info-section">
              <p><strong>Subject:</strong> {{ quizDetails.subject_name }}</p>
              <p><strong>Chapter:</strong> {{ quizDetails.chapter_name }}</p>
              <p><strong>Date:</strong> {{ quizDetails.quiz_date }}</p>
            </div>
            <div class="quiz-info-section">
              <p><strong>Duration:</strong> {{ quizDetails.time_duration }} minutes</p>
              <p><strong>Total Questions:</strong> {{ questions.length }}</p>
              <p><strong>Total Marks:</strong> {{ questions.reduce((sum, q) => sum + q.max_marks, 0) }}</p>
            </div>
          </div>
          <p v-if="quizDetails.remarks" class="quiz-remarks"><strong>Remarks:</strong> {{ quizDetails.remarks }}</p>
        </div>

        <!-- Questions List -->
        <div class="questions-container">
          <div v-if="loadingQuestions" class="loading-state">
            Loading questions...
          </div>
          
          <div v-else-if="questions.length === 0" class="no-questions-state">
            No questions added yet.
          </div>
          
          <div v-else class="questions-list">
            <div v-for="(question, index) in questions" 
                 :key="question.id" 
                 class="question-item">
              <div class="question-header">
                <h5 v-html="question.question"></h5>
                <div class="question-actions">
                  <span class="marks-badge">{{ question.max_marks }} marks</span>
                  <button 
                    class="action-btn edit-btn" 
                    @click.stop="handleEditClick(question)"
                    title="Edit question"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button 
                    class="action-btn delete-btn" 
                    @click.stop="deleteQuestion(question.id)"
                    title="Delete question"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
              
              <div class="options-list">
                <div v-for="option in question.options" 
                     :key="option.id"
                     :class="['option-item', { 'correct-option': option.is_correct }]">
                  {{ option.option_text }}
                </div>
              </div>
              
              <hr v-if="index < questions.length - 1" class="question-divider">
            </div>
          </div>
        </div>

        <button class="add-question-btn" @click="addQuestion">
          <i class="bi bi-plus-circle"></i>
          Add Question
        </button>
      </div>
      <div v-else class="loading-state">
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
.admin-quiz-edit-container {
  padding: 2rem;
  min-height: 100vh;
}

.selected-quiz {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.selected-quiz:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.quiz-header h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.quiz-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.edit-btn {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.delete-btn {
  background: linear-gradient(45deg, #dc3545 0%, #c82333 100%);
  color: white;
}

.quiz-details {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1.5rem;
  border-radius: 15px;
  margin-bottom: 2rem;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.quiz-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.quiz-info-section p {
  margin-bottom: 0.75rem;
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

.quiz-info-section strong {
  color: #667eea;
  font-weight: 700;
}

.quiz-remarks {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

.quiz-remarks strong {
  color: #667eea;
  font-weight: 700;
}

.questions-container {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.questions-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.loading-state, .no-questions-state {
  text-align: center;
  padding: 3rem 2rem;
  font-size: 1.2rem;
  color: #666;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  border: 1px solid #e0e0e0;
}

.question-item {
  padding: 1.5rem 0;
  transition: all 0.3s ease;
}

.question-item:hover {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  padding: 1.5rem;
  margin: 0 -1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.question-header h5 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  flex: 1;
  line-height: 1.5;
}

.question-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.marks-badge {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.options-list {
  padding-left: 1.5rem;
}

.option-item {
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  border-radius: 10px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  font-weight: 500;
}

.option-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.correct-option {
  background: linear-gradient(45deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border-left: 4px solid #28a745;
  font-weight: 700;
}

.question-divider {
  border-top: 1px solid #f0f0f0;
  margin: 2rem 0;
}

.add-question-btn {
  background: linear-gradient(45deg, #28a745 0%, #218838 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.add-question-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.add-question-btn i {
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .admin-quiz-edit-container {
    padding: 1.5rem;
  }
  
  .selected-quiz {
    padding: 1.5rem;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .quiz-header h2 {
    font-size: 1.5rem;
  }
  
  .quiz-info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .question-actions {
    align-self: flex-end;
  }
  
  .questions-container {
    padding: 1.5rem;
  }
}
</style>