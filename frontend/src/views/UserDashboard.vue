<template>
  <div class="user-dashboard">
    <div class="welcome-section">
      <h1>Hi, {{ user}}</h1>
            
    </div>

    <!-- Search Component -->
    <QuizSearch 
      v-if="!loading && !error"
      :quizzes="allQuizzes" 
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { fetchCatalogData } from '@/utils/catalogData';
import QuizList from '@/components/quiz/QuizList.vue';
import QuizSearch from '@/components/quiz/QuizSearch.vue';

const authStore = useAuthStore();
const user = ref(authStore.user);

// Quiz data refs
const ongoingQuizzes = ref([]);
const upcomingQuizzes = ref([]);
const previousQuizzes = ref([]);
const loading = ref(true);
const error = ref(null);

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
  padding: 2rem;
}

.welcome-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.welcome-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.welcome-section h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.quizzes-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 20px;
  margin: 1rem 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  font-size: 1.2rem;
  color: #666;
}

.error-state {
  color: #dc3545;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border: 1px solid #f5c6cb;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(45deg, #6c757d 0%, #5a6268 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
}

@media (max-width: 768px) {
  .user-dashboard {
    padding: 1.5rem;
  }
  
  .welcome-section {
    padding: 1.25rem;
  }
  
  .welcome-section h1 {
    font-size: 1.75rem;
  }
  
  .loading-state,
  .error-state {
    padding: 2rem 1.5rem;
    font-size: 1.1rem;
  }
}
</style>
