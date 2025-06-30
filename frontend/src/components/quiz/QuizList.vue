<template>
  <section v-if="quizzes.length > 0" class="quiz-section">
    <h2>{{ sectionTitle }}</h2>
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
    validator: (value) => ['ongoing', 'upcoming', 'previous'].includes(value)
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
  margin-bottom: 30px;
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
  margin-bottom: 20px;
}

.no-quizzes {
  text-align: center;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin: 1rem 0;
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.page-numbers {
  display: flex;
  gap: 5px;
}

.pagination-btn, 
.page-btn {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.7;
}

.pagination-btn:not(:disabled):hover,
.page-btn:hover {
  background-color: #f5f5f5;
}

.page-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

@media (max-width: 768px) {
  .pagination {
    flex-wrap: wrap;
  }
  
  .page-numbers {
    order: 2;
    width: 100%;
    justify-content: center;
    margin-top: 10px;
  }
  
  .pagination-btn {
    order: 1;
  }
}
</style> 