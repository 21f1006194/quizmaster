<template>
  <div class="user-dashboard">
    <div class="welcome-section">
      <div class="welcome-header">
        <h1>Quiz Management</h1>
        <button 
          class="btn btn-primary new-quiz-btn"
          @click="showCreateModal = true"
        >
          <i class="bi bi-plus-circle"></i>
          New Quiz
        </button>
      </div>
    </div>

    <!-- Search Component -->
    <QuizSearch 
      v-if="!loading && !error"
      :quizzes="allQuizzes"
      :initial-search="searchQuery"
    />

    <div class="quizzes-section">
      <div v-if="loading" class="loading-state">
        <p>Loading quizzes...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="loadQuizData" class="retry-btn">Retry</button>
      </div>

      <template v-else>
        <QuizList
          :quizzes="ongoingQuizzes"
          section-title="Ongoing Quizzes"
          section-type="ongoing"
        />

        <QuizList
          :quizzes="upcomingQuizzes"
          section-title="Upcoming Quizzes"
          section-type="upcoming"
        />

        <QuizList
          :quizzes="previousQuizzes"
          section-title="Previous Quizzes"
          section-type="previous"
        />
      </template>
    </div>

    <!-- Quiz Form Modal -->
    <QuizFormModal
      :show="showCreateModal"
      mode="create"
      @close="showCreateModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { fetchCatalogData } from '@/utils/catalogData';
import QuizList from '@/components/quiz/QuizList.vue';
import QuizSearch from '@/components/quiz/QuizSearch.vue';
import QuizFormModal from '@/components/modals/QuizFormModal.vue';
import { useRoute } from 'vue-router';

const authStore = useAuthStore();
const user = ref(authStore.user);

const route = useRoute();
const searchQuery = ref(route.query.search || '');

// Quiz data refs
const ongoingQuizzes = ref([]);
const upcomingQuizzes = ref([]);
const previousQuizzes = ref([]);
const loading = ref(true);
const error = ref(null);
const showCreateModal = ref(false);

// Computed property for all quizzes
const allQuizzes = computed(() => [
  ...ongoingQuizzes.value,
  ...upcomingQuizzes.value,
  ...previousQuizzes.value
]);

// Function to categorize quizzes based on their dates
const categorizeQuizzes = (quizzes) => {
  const now = new Date();
  const ongoing = [];
  const upcoming = [];
  const previous = [];

  quizzes.forEach(quiz => {
    const quizDate = new Date(quiz.quiz_date);
    const endDate = new Date(quizDate.getTime() + quiz.time_duration * 60000); // Convert minutes to milliseconds

    // Format the quiz object with consistent structure
    const formattedQuiz = {
      id: quiz.id,
      title: quiz.title,
      subject: quiz.subject_name,
      chapter: quiz.chapter_name,
      duration: quiz.time_duration,
      date: quiz.quiz_date,
      time: quizDate.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      }),
      remarks: quiz.remarks
    };

    if (now >= quizDate && now <= endDate) {
      ongoing.push(formattedQuiz);
    } else if (now < quizDate) {
      upcoming.push(formattedQuiz);
    } else {
      previous.push(formattedQuiz);
    }
  });

  return { ongoing, upcoming, previous };
};

// Function to extract all quizzes from the catalog data
const extractQuizzes = (catalogData) => {
  const allQuizzes = [];
  
  catalogData.subjects.forEach(subject => {
    subject.chapters.forEach(chapter => {
      if (chapter.quizzes && chapter.quizzes.length > 0) {
        chapter.quizzes.forEach(quiz => {
          allQuizzes.push({
            ...quiz,
            subject_name: subject.name,
            chapter_name: chapter.name
          });
        });
      }
    });
  });

  return allQuizzes;
};

// Function to load and process quiz data
const loadQuizData = async () => {
  try {
    loading.value = true;
    error.value = null;

    const { data, error: fetchError } = await fetchCatalogData();
    
    if (fetchError) {
      throw new Error(fetchError);
    }

    const allQuizzes = extractQuizzes(data);
    const { ongoing, upcoming, previous } = categorizeQuizzes(allQuizzes);

    ongoingQuizzes.value = ongoing;
    upcomingQuizzes.value = upcoming;
    previousQuizzes.value = previous;
  } catch (err) {
    error.value = err.message || 'Failed to load quiz data';
    console.error('Error loading quiz data:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadQuizData();
});
</script>

<style scoped>
.user-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-section {
  margin-bottom: 30px;
}

.welcome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-header h1 {
  font-size: 28px;
  font-weight: 600;
  margin: 0; /* Remove default margin to ensure proper alignment */
}

.quizzes-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin: 1rem 0;
}

.error-state {
  color: #dc3545;
}

.retry-btn {
  margin-top: 1rem;
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #5a6268;
}

.new-quiz-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>