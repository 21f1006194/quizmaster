<template>
  <div class="search-section">
    <div class="search-container">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search quizzes..." 
          @input="searchQuizzes"
        />
      </div>
      <div class="date-picker">
        <input 
          type="date" 
          v-model="selectedDate"
          @change="searchQuizzes"
        />
      </div>
      <button class="help-button" @click="showHelpModal = true">
        <i class="bi bi-question-circle"></i>
      </button>
    </div>

    <!-- Search Results -->
    <div v-if="(searchQuery || selectedDate) && filteredQuizzes.length > 0" 
         class="search-results-container">
      <QuizList
        :quizzes="filteredQuizzes"
        section-title="Search Results"
        section-type="search"
      />
    </div>

    <!-- Help Modal -->
    <SearchHelpModal v-model="showHelpModal" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import QuizList from './QuizList.vue';
import SearchHelpModal from './SearchHelpModal.vue';
import { QueryParser } from '@/utils/queryParser';

const props = defineProps({
  quizzes: {
    type: Array,
    required: true
  },
  initialSearch: {
    type: String,
    default: ''
  }
});

const searchQuery = ref(props.initialSearch);
const selectedDate = ref('');
const filteredQuizzes = ref([]);
const showHelpModal = ref(false);
const queryParser = new QueryParser();

// Define searchQuizzes first
const searchQuizzes = () => {
  if (!searchQuery.value.trim() && !selectedDate.value) {
    filteredQuizzes.value = [];
    return;
  }

  const parsedQuery = queryParser.parse(searchQuery.value);
  
  filteredQuizzes.value = props.quizzes.filter(quiz => {
    // Apply date filter from date picker if selected
    if (selectedDate.value) {
      const quizDate = new Date(quiz.date);
      const filterDate = new Date(selectedDate.value);
      const matchesDate = 
        quizDate.getFullYear() === filterDate.getFullYear() &&
        quizDate.getMonth() === filterDate.getMonth() &&
        quizDate.getDate() === filterDate.getDate();
      
      if (!matchesDate) return false;
    }

    // If no parsed query, return true (only date filter applied)
    if (!parsedQuery) return true;

    // Apply filters from query
    for (const filter of parsedQuery.filters) {
      if (filter.type === 'DATE_FILTER') {
        const quizDate = new Date(quiz.date);
        const filterDate = new Date(filter.value);
        
        if (filter.field === 'after' && quizDate < filterDate) return false;
        if (filter.field === 'before' && quizDate > filterDate) return false;
      }
      
      if (filter.type === 'DURATION_FILTER') {
        const duration = quiz.duration;
        const filterValue = filter.value;
        
        switch (filterValue.type) {
          case 'RANGE':
            if (duration < filterValue.min || duration > filterValue.max) return false;
            break;
          case 'GREATER_THAN':
            if (duration <= filterValue.value) return false;
            break;
          case 'LESS_THAN':
            if (duration >= filterValue.value) return false;
            break;
          case 'EXACT':
            if (duration !== filterValue.value) return false;
            break;
        }
      }
    }

    // Apply search terms
    let matches = true;
    let hasOrMatch = false;

    for (let i = 0; i < parsedQuery.terms.length; i++) {
      const term = parsedQuery.terms[i];
      const operator = parsedQuery.operators[i] || 'AND';
      
      const termMatches = evaluateTerm(term, quiz);
      
      if (operator === 'OR') {
        hasOrMatch = hasOrMatch || termMatches;
      } else {
        matches = matches && termMatches;
      }
    }

    return matches && (parsedQuery.operators.length === 0 || hasOrMatch);
  });
};

// Use onMounted instead of watch to trigger initial search
onMounted(() => {
  if (props.initialSearch) {
    searchQuizzes();
  }
});

const evaluateTerm = (term, quiz) => {
  const searchValue = term.value.toLowerCase();
  
  switch (term.type) {
    case 'EXACT_PHRASE':
      return (
        quiz.title.toLowerCase().includes(searchValue) ||
        quiz.subject.toLowerCase().includes(searchValue) ||
        quiz.chapter.toLowerCase().includes(searchValue) ||
        (quiz.remarks && quiz.remarks.toLowerCase().includes(searchValue))
      );
      
    case 'FIELD_SEARCH':
      const fieldValue = quiz[term.field]?.toLowerCase() || '';
      return fieldValue.includes(searchValue);
      
    case 'NOT':
      return !(
        quiz.title.toLowerCase().includes(searchValue) ||
        quiz.subject.toLowerCase().includes(searchValue) ||
        quiz.chapter.toLowerCase().includes(searchValue) ||
        (quiz.remarks && quiz.remarks.toLowerCase().includes(searchValue))
      );
      
    case 'TERM':
    default:
      return (
        quiz.title.toLowerCase().includes(searchValue) ||
        quiz.subject.toLowerCase().includes(searchValue) ||
        quiz.chapter.toLowerCase().includes(searchValue) ||
        (quiz.remarks && quiz.remarks.toLowerCase().includes(searchValue))
      );
  }
};
</script>

<style scoped>
.search-section {
  margin-bottom: 20px;
}

.search-container {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  flex: 1;
}

.search-bar input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background-color: #f9f9f9;
}

.date-picker input {
  padding: 11px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background-color: #f9f9f9;
  cursor: pointer;
}

.date-picker input::-webkit-calendar-picker-indicator {
  cursor: pointer;
}

.help-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 8px;
  transition: color 0.2s;
}

.help-button:hover {
  color: #333;
}

.search-results-container {
  background-color: #edeeee;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  margin-top: 10px;  /* Add space between search bar and results */
  margin-bottom: 30px;
}
</style> 