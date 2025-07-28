<template>
  <section v-if="quizzes.length > 0" 
    :class="['quiz-section', { 'search-results': sectionType === 'search' }]">
    <h2>
      {{ sectionTitle }}
      <span v-if="sectionType === 'search'" class="result-count">
        ({{ quizzes.length }} results found)
      </span>
    </h2>
    <div class="quiz-list">
      <!-- Emit the emits for now, will handle later TODO -->
      <QuizCard
        v-for="quiz in paginatedQuizzes"
        :key="quiz.id"
        :quiz="quiz"
        :quiz-state="sectionType"
        @reminder-set="$emit('reminder-set', $event)"
        @view-results="$emit('view-results', $event)"
        @edit-quiz="$emit('edit-quiz', $event)"
      />
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn" 
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        Previous
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in totalPages" 
          :key="page"
          :class="['page-btn', { active: page === currentPage }]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>

      <button 
        class="pagination-btn" 
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Next
      </button>
    </div>
  </section>
  <div v-else class="no-quizzes">
    <p>No {{ sectionType }} quizzes available.</p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import QuizCard from './QuizCard.vue';

const props = defineProps({
  quizzes: {
    type: Array,
    required: true
  },
  sectionTitle: {
    type: String,
    required: true
  },
  sectionType: {
    type: String,
    required: true,
    validator: (value) => ['ongoing', 'upcoming', 'previous', 'search'].includes(value)
  }
});

defineEmits(['reminder-set', 'view-results', 'edit-quiz']);

// Pagination
const itemsPerPage = 5;
const currentPage = ref(1);

// Calculate total pages
const totalPages = computed(() => Math.ceil(props.quizzes.length / itemsPerPage));

// Get paginated quizzes
const paginatedQuizzes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return props.quizzes.slice(start, end);
});

// Watch for quizzes changes to reset pagination
watch(() => props.quizzes, () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.quiz-section {
  margin-bottom: 2rem;
}

.quiz-section h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.no-quizzes {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 20px;
  margin: 1rem 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  color: #666;
  font-size: 1.1rem;
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.pagination-btn, 
.page-btn {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.875rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.pagination-btn:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}

.pagination-btn:not(:disabled):hover,
.page-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.page-btn.active {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .pagination {
    flex-wrap: wrap;
  }
  
  .page-numbers {
    order: 2;
    width: 100%;
    justify-content: center;
    margin-top: 1rem;
  }
  
  .pagination-btn {
    order: 1;
  }
  
  .quiz-section h2 {
    font-size: 1.5rem;
  }
}

.quiz-section.search-results {
  padding: 2rem;
  border-radius: 20px;
  border: 1px solid #f0f0f0;
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.result-count {
  font-size: 1rem;
  color: #666;
  font-weight: 500;
  margin-left: 0.75rem;
}
</style> 