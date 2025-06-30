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
    </div>

    <!-- Search Results -->
    <QuizList
      v-if="(searchQuery || selectedDate) && filteredQuizzes.length > 0"
      :quizzes="filteredQuizzes"
      section-title="Search Results"
      section-type="search"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import QuizList from './QuizList.vue';

const props = defineProps({
  quizzes: {
    type: Array,
    required: true
  }
});

const searchQuery = ref('');
const selectedDate = ref('');
const filteredQuizzes = ref([]);

const searchQuizzes = () => {
  if (!searchQuery.value.trim() && !selectedDate.value) {
    filteredQuizzes.value = [];
    return;
  }

  const query = searchQuery.value.toLowerCase();
  
  filteredQuizzes.value = props.quizzes.filter(quiz => {
    // If there's a search query, check for matches
    const matchesSearch = !query || 
      quiz.title.toLowerCase().includes(query) ||
      quiz.subject.toLowerCase().includes(query) ||
      quiz.chapter.toLowerCase().includes(query);

    // If there's a selected date, check for date match
    if (selectedDate.value) {
      const quizDate = new Date(quiz.date);
      const filterDate = new Date(selectedDate.value);
      const matchesDate = 
        quizDate.getFullYear() === filterDate.getFullYear() &&
        quizDate.getMonth() === filterDate.getMonth() &&
        quizDate.getDate() === filterDate.getDate();
      
      // If there's a search query, both conditions must match
      // If there's no search query, only date needs to match
      return query ? (matchesSearch && matchesDate) : matchesDate;
    }

    // If no date selected, return search matches
    return matchesSearch;
  });
};
</script>

<style scoped>
.search-section {
  margin-bottom: 30px;
}

.search-container {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 15px;
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
</style> 