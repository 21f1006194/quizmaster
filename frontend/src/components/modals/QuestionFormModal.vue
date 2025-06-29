<script setup>
import { ref, watch } from 'vue';
import api from '@/api';

const props = defineProps({
  show: Boolean,
  quizId: Number,
  question: {
    type: Object,
    default: null
  },
  isEditing: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'question-added', 'question-updated']);

const questionText = ref('');
const maxMarks = ref(1.0);
const options = ref([
  { text: '', is_correct: false },
  { text: '', is_correct: false },
  { text: '', is_correct: false },
  { text: '', is_correct: false }
]);

const error = ref('');
const loading = ref(false);

watch(() => props.show, (newVal) => {
  if (newVal) {
    if (props.isEditing && props.question) {
      questionText.value = props.question.question;
      maxMarks.value = props.question.max_marks;
      options.value = props.question.options.map(opt => ({
        text: opt.option_text,
        is_correct: opt.is_correct
      }));
    } else {
      questionText.value = '';
      maxMarks.value = 1.0;
      options.value = Array(4).fill().map(() => ({
        text: '',
        is_correct: false
      }));
    }
    error.value = '';
  }
});

const handleOptionCorrectChange = (index) => {
  options.value = options.value.map((opt, i) => ({
    ...opt,
    is_correct: i === index
  }));
};

const validateForm = () => {
  if (!questionText.value.trim()) {
    error.value = 'Question text is required';
    return false;
  }
  
  if (maxMarks.value <= 0) {
    error.value = 'Max marks must be greater than 0';
    return false;
  }

  const filledOptions = options.value.filter(opt => opt.text.trim());
  if (filledOptions.length < 2) {
    error.value = 'At least 2 options are required';
    return false;
  }

  if (!options.value.some(opt => opt.is_correct)) {
    error.value = 'Please mark one option as correct';
    return false;
  }

  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  try {
    loading.value = true;
    error.value = '';

    const questionData = {
      question: questionText.value,
      max_marks: maxMarks.value,
      options: options.value
        .filter(opt => opt.text.trim())
        .map(opt => ({
          option_text: opt.text,
          is_correct: opt.is_correct
        }))
    };

    if (props.isEditing) {
      const response = await api.put(`/admin/api/questions/${props.question.id}`, questionData);
      emit('question-updated', response.data);
    } else {
      const response = await api.post(`/admin/api/quiz/${props.quizId}/questions`, questionData);
      emit('question-added', response.data);
    }

    emit('close');
  } catch (err) {
    error.value = err.response?.data?.msg || 'Failed to save question';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div v-if="show" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEditing ? 'Edit Question' : 'Add New Question' }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          
          <div class="mb-3">
            <label class="form-label">Question</label>
            <textarea 
              class="form-control" 
              v-model="questionText"
              rows="3"
              placeholder="Enter your question here"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Max Marks</label>
            <input 
              type="number" 
              class="form-control" 
              v-model="maxMarks"
              min="0.5"
              step="0.5"
            >
          </div>

          <div class="options-section">
            <label class="form-label">Options</label>
            <div v-for="(option, index) in options" :key="index" class="option-row mb-3">
              <div class="d-flex gap-3 align-items-center">
                <div class="flex-grow-1">
                  <input 
                    type="text" 
                    class="form-control"
                    v-model="option.text"
                    :placeholder="`Option ${index + 1}`"
                  >
                </div>
                <div class="form-check">
                  <input 
                    type="radio" 
                    name="correct-option" 
                    class="form-check-input"
                    :checked="option.is_correct"
                    @change="handleOptionCorrectChange(index)"
                  >
                  <label class="form-check-label">Correct</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            Cancel
          </button>
          <button 
            type="button"
            class="btn btn-primary" 
            @click="handleSubmit"
            :disabled="loading"
          >
            {{ loading ? 'Saving...' : (isEditing ? 'Update' : 'Save') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  z-index: 1050;
}

.option-row {
  padding: 10px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}
</style> 