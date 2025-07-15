<template>
  <div v-if="modelValue" class="modal-overlay" @click="$emit('update:modelValue', false)">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Advanced Search Guide</h2>
        <button class="close-button" @click="$emit('update:modelValue', false)">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <div class="search-guide">
          <h3>Basic Search</h3>
          <p>By default, spaces between words use AND logic:</p>
          <code>math science</code>
          <p>Finds quizzes containing both "math" and "science" in any field.</p>

          <h3>OR Logic</h3>
          <p>Use | (with spaces) to find results containing either keyword:</p>
          <code>(math | science) easy</code>
          <p>Finds quizzes with "math" or "science" that also include "easy".</p>

          <h3>Exact Phrase</h3>
          <p>Use quotes for an exact match:</p>
          <code>"math quiz"</code>
          <p>Finds quizzes containing the exact phrase "math quiz".</p>

          <h3>Field-Specific Search</h3>
          <p>Search in specific fields using field:keyword:</p>
          <ul>
            <li><code>subject:algebra</code> - Search in subject field</li>
            <li><code>chapter:functions</code> - Search in chapter field</li>
            <li><code>title:quiz</code> - Search in title field</li>
          </ul>

          <h3>Date Filters</h3>
          <p>Filter quizzes by date:</p>
          <ul>
            <li><code>after:2024-01-01</code> - Find quizzes after January 1, 2024</li>
            <li><code>before:2024-12-31</code> - Find quizzes before December 31, 2024</li>
          </ul>

          <h3>Duration Filters</h3>
          <p>Filter quizzes by duration:</p>
          <ul>
            <li><code>duration:15</code> - Find quizzes lasting exactly 15 minutes</li>
            <li><code>duration:>30</code> - Find quizzes longer than 30 minutes</li>
            <li><code>duration:<20</code> - Find quizzes shorter than 20 minutes</li>
            <li><code>duration:15-30</code> - Find quizzes between 15 and 30 minutes</li>
          </ul>

          <h3>Excluding Words</h3>
          <p>Use -keyword to exclude a word:</p>
          <code>math -calculus</code>
          <p>Finds "math" quizzes but excludes those containing "calculus".</p>

          <h3>Combining Filters</h3>
          <p>You can combine multiple filters:</p>
          <code>subject:math duration:15-30 after:2024-01-01</code>
          <p>Finds math quizzes lasting 15-30 minutes created after January 1, 2024.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
}

.close-button:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.search-guide {
  color: #444;
}

.search-guide h3 {
  color: #333;
  margin-top: 24px;
  margin-bottom: 12px;
  font-size: 18px;
}

.search-guide p {
  margin: 8px 0;
  line-height: 1.5;
}

.search-guide code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: #e83e8c;
  display: inline-block;
  margin: 4px 0;
}

.search-guide ul {
  margin: 8px 0;
  padding-left: 20px;
}

.search-guide li {
  margin: 4px 0;
  line-height: 1.5;
}

.search-guide li code {
  margin: 0;
}
</style> 