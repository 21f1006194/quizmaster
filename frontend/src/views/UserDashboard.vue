<template>
  <div class="user-dashboard">
    <div class="welcome-section">
      <h1>Hi, {{ user?.name || 'User' }}</h1>
    </div>

    <div class="search-section">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search quizzes..." 
          @input="searchQuizzes"
        />
      </div>
    </div>

    <div class="quizzes-section">
      <div v-if="loading" class="loading-state">
        <p>Loading quizzes...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="loadQuizData" class="retry-btn">Retry</button>
      </div>

      <template v-else>
        <section v-if="ongoingQuizzes.length > 0" class="quiz-section ongoing">
          <h2>Ongoing Quizzes</h2>
          <div class="quiz-list">
            <div v-for="quiz in ongoingQuizzes" :key="quiz.id" class="quiz-item">
              <div class="quiz-info">
                <div class="quiz-time">
                  <span class="icon">⏱️</span>
                </div>
                <div class="quiz-details">
                  <h3>{{ quiz.title }}</h3>
                  <p>{{ quiz.subject }} | {{ quiz.chapter }}</p>
                  <p class="quiz-metadata">
                    Duration: {{ quiz.duration }} minutes | 
                    Start Time: {{ new Date(quiz.date).toLocaleString() }}
                  </p>
                  <p v-if="quiz.remarks" class="quiz-remarks">{{ quiz.remarks }}</p>
                </div>
              </div>
              <button class="action-btn start" @click="$router.push(`/user/attempt-quiz/${quiz.id}`)">
                Start Quiz
              </button>
            </div>
          </div>
        </section>

        <section v-if="upcomingQuizzes.length > 0" class="quiz-section upcoming">
          <h2>Upcoming Quizzes</h2>
          <div class="quiz-list">
            <div v-for="quiz in upcomingQuizzes" :key="quiz.id" class="quiz-item">
              <div class="quiz-info">
                <div class="quiz-time">
                  <span class="icon">⏱️</span>
                </div>
                <div class="quiz-details">
                  <h3>{{ quiz.title }}</h3>
                  <p>{{ quiz.subject }} | {{ quiz.chapter }}</p>
                  <p class="quiz-metadata">
                    Duration: {{ quiz.duration }} minutes | 
                    Start Time: {{ new Date(quiz.date).toLocaleString() }}
                  </p>
                  <p v-if="quiz.remarks" class="quiz-remarks">{{ quiz.remarks }}</p>
                </div>
              </div>
              <button class="action-btn reminder">Set Reminder</button>
            </div>
          </div>
        </section>

        <section v-if="previousQuizzes.length > 0" class="quiz-section previous">
          <h2>Previous Quizzes</h2>
          <div class="quiz-list">
            <div v-for="quiz in previousQuizzes" :key="quiz.id" class="quiz-item">
              <div class="quiz-info">
                <div class="quiz-time">
                  <span class="icon">⏱️</span>
                </div>
                <div class="quiz-details">
                  <h3>{{ quiz.title }}</h3>
                  <p>{{ quiz.subject }} | {{ quiz.chapter }}</p>
                  <p class="quiz-metadata">
                    Duration: {{ quiz.duration }} minutes | 
                    Start Time: {{ new Date(quiz.date).toLocaleString() }}
                  </p>
                  <p v-if="quiz.remarks" class="quiz-remarks">{{ quiz.remarks }}</p>
                </div>
              </div>
              <button class="action-btn results">See Results</button>
            </div>
          </div>
        </section>

        <div v-if="!ongoingQuizzes.length && !upcomingQuizzes.length && !previousQuizzes.length" class="no-quizzes">
          <p>No quizzes available at the moment.</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { fetchCatalogData } from '@/utils/catalogData';

const authStore = useAuthStore();
const user = ref(authStore.user);
const searchQuery = ref('');

// Quiz data refs
const ongoingQuizzes = ref([]);
const upcomingQuizzes = ref([]);
const previousQuizzes = ref([]);
const loading = ref(true);
const error = ref(null);

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

const searchQuizzes = () => {
  // TODO: Implement search functionality
  // This will filter through ongoingQuizzes, upcomingQuizzes, and previousQuizzes
  // based on the searchQuery.value
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

.welcome-section h1 {
  font-size: 28px;
  font-weight: 600;
}

.search-section {
  margin-bottom: 30px;
}

.search-bar {
  margin-bottom: 15px;
}

.search-bar input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background-color: #f9f9f9;
}

.quizzes-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.quiz-section h2 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 15px;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.quiz-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.quiz-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.quiz-time {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
}

.quiz-details h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 5px;
}

.quiz-details p {
  font-size: 14px;
  color: #666;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.action-btn.start {
  background-color: #28a745;
  color: white;
}

.action-btn.reminder {
  background-color: #6c757d;
  color: white;
}

.action-btn.results {
  background-color: #007bff;
  color: white;
}

.icon {
  display: inline-block;
  margin-right: 2px;
}

@media (max-width: 768px) {
  .quiz-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .action-btn {
    align-self: flex-end;
  }
}

.quiz-metadata {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}

.quiz-remarks {
  font-size: 13px;
  color: #666;
  font-style: italic;
  margin-top: 4px;
}

.loading-state,
.error-state,
.no-quizzes {
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
</style>
