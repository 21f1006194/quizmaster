<script setup>
import { ref, onMounted, watch } from 'vue';
import { fetchCatalogData } from '@/utils/catalogData';
import api from '@/api';
import QuestionFormModal from '@/components/modals/QuestionFormModal.vue';

const organizedData = ref({ subjects: [] });
const selectedSubject = ref(null);
const selectedQuiz = ref(null);
const loading = ref(true);
const questions = ref([]);
const loadingQuestions = ref(false);
const showQuestionModal = ref(false);
const editingQuestion = ref(null);

const loadData = async () => {
  try {
    loading.value = true;
    const { data, error } = await fetchCatalogData();
    if (error) throw new Error(error);
    organizedData.value = data;
  } catch (error) {
    console.error('Error loading data:', error);
  } finally {
    loading.value = false;
  }
};

const fetchQuestions = async (quizId) => {
  try {
    loadingQuestions.value = true;
    const response = await api.get(`/admin/api/quiz/${quizId}/questions`);
    questions.value = response.data.questions;
  } catch (error) {
    console.error('Error fetching questions:', error);
  } finally {
    loadingQuestions.value = false;
  }
};

const handleSubjectChange = (subjectId) => {
  selectedSubject.value = subjectId;
  selectedQuiz.value = null;
};

const handleQuizSelect = async (quiz) => {
  selectedQuiz.value = quiz;
  await fetchQuestions(quiz.id);
};

const addQuestion = () => {
  showQuestionModal.value = true;
};

const handleQuestionAdded = async (newQuestion) => {
  await fetchQuestions(selectedQuiz.value.id);
};

const deleteQuestion = async (questionId) => {
  if (!confirm('Are you sure you want to delete this question?')) {
    return;
  }

  try {
    await api.delete(`/admin/api/questions/${questionId}`);
    // Refresh questions list after deletion
    await fetchQuestions(selectedQuiz.value.id);
  } catch (error) {
    console.error('Error deleting question:', error);
    alert('Failed to delete question');
  }
};

const handleEditClick = (question) => {
  editingQuestion.value = question;
  showQuestionModal.value = true;
};

const handleQuestionUpdated = async (updatedQuestion) => {
  await fetchQuestions(selectedQuiz.value.id);
  editingQuestion.value = null;
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="admin-quiz-container">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="subject-selector mb-3">
        <select 
          class="form-select" 
          v-model="selectedSubject"
          @change="handleSubjectChange(selectedSubject)"
        >
          <option value="">Select Subject</option>
          <option 
            v-for="subject in organizedData.subjects" 
            :key="subject.id" 
            :value="subject.id"
          >
            {{ subject.name }}
          </option>
        </select>
      </div>

      <div class="quiz-list" v-if="selectedSubject">
        <div 
          v-for="chapter in organizedData.subjects.find(s => s.id === selectedSubject)?.chapters" 
          :key="chapter.id" 
          class="chapter-section"
        >
        
          <div class="chapter-header d-flex justify-content-between align-items-center" @click="chapter.isCollapsed = !chapter.isCollapsed">
            <h6 class="chapter-title mb-0">{{ chapter.name }}</h6>
            <i class="bi" :class="chapter.isCollapsed ? 'bi-chevron-down' : 'bi-chevron-up'"></i>
          </div>
          <ul class="list-unstyled" v-show="!chapter.isCollapsed">
            <li 
              v-for="quiz in chapter.quizzes" 
              :key="quiz.id"
              :class="['quiz-item', { active: selectedQuiz?.id === quiz.id }]"
              @click="handleQuizSelect(quiz)"
            >
              {{ quiz.title }}
            </li>
            <li v-if="chapter.quizzes.length === 0" class="no-quizzes">
              No quizzes in this chapter
            </li>
          </ul>
        </div>
      </div>

      <div v-if="loading" class="text-center">
        Loading...
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div v-if="selectedQuiz" class="selected-quiz">
        <h2>{{ selectedQuiz.title }}</h2>
        <div class="d-flex align-items-start justify-content-between mb-4">
          <div class="d-flex flex-column">
            <span class="text-muted mb-2">Date: {{ selectedQuiz.quiz_date }}</span>
            <span class="text-muted">Questions: {{ questions.length }}</span>
          </div>
          <div class="d-flex flex-column">
            <span class="text-muted mb-2">Duration: {{ selectedQuiz.time_duration }} minutes</span>
            <span class="text-muted">Total Marks: {{ questions.reduce((sum, q) => sum + q.max_marks, 0) }}</span>
          </div>
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
        Please select a quiz from the sidebar
      </div>
    </div>
  </div>

  <QuestionFormModal
    :show="showQuestionModal"
    :quiz-id="selectedQuiz?.id"
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

.sidebar {
  width: 300px;
  padding: 20px;
  background-color: #f8f9fa;
  border-right: 1px solid #dee2e6;
  overflow-y: auto;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
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
</style>