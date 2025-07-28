<script setup>
import { ref, watch } from 'vue';
import api from '@/api';
import QuizEditor from '@/components/QuizEditor.vue';

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
            <QuizEditor v-model="questionText" />
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

.modal-content {
  border-radius: 20px;
  border: none;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px 20px 0 0;
  border-bottom: none;
  padding: 1.5rem 2rem;
}

.modal-title {
  font-weight: 600;
  margin: 0;
}

.btn-close {
  filter: invert(1);
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.btn-close:hover {
  opacity: 1;
}

.modal-body {
  padding: 2rem;
}

.form-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-control {
  border-radius: 10px;
  border: 2px solid #e0e0e0;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #f0f0f0;
  border-radius: 0 0 20px 20px;
}

.btn {
  border-radius: 50px;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.alert-danger {
  border-radius: 10px;
  border: none;
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
}

.option-row {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.option-row:hover {
  border-color: #667eea;
  background-color: #f8f9fa;
}

.form-check-input {
  border-radius: 50%;
  border: 2px solid #667eea;
  transition: all 0.3s ease;
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}

.form-check-label {
  font-weight: 600;
  color: #333;
  margin-left: 0.5rem;
}
</style> 