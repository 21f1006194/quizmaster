<script setup>
import { ref, watch } from 'vue';
import api from '@/api';

const props = defineProps({
  show: Boolean,
  chapter: Object,
  subjectId: Number,  
  isEditing: Boolean  
});

const emit = defineEmits(['close', 'chapter-updated', 'chapter-added']);

const error = ref('');
const chapterForm = ref({
  name: '',
  description: ''
});

// Watch both show and chapter props
// Using watch is not strictly necessary here, but I'm using it since it's a good practice.
watch(
  [() => props.show, () => props.chapter],
  ([newShow, newChapter]) => {
    if (newShow && props.isEditing && newChapter) {
      // Populate form when modal opens for editing
      chapterForm.value = {
        name: newChapter.name,
        description: newChapter.description
      };
    } else if (!newShow) {
      // Reset form when modal closes
      chapterForm.value = {
        name: '',
        description: ''
      };
    }
  }
);

const saveChapter = async () => {
  try {
    if (props.isEditing) {
      await api.put(`/admin/api/chapters/${props.chapter.id}`, chapterForm.value);
      emit('chapter-updated');
    } else {
      await api.post(`/admin/api/subjects/${props.subjectId}/chapters`, chapterForm.value);
      emit('chapter-added');
    }
    closeModal();
  } catch (err) {
    error.value = `Failed to ${props.isEditing ? 'update' : 'create'} chapter.`;
    console.error(err);
  }
};

const closeModal = () => {
  error.value = '';
  emit('close');
};
</script>

<template>
  <div v-if="show" class="modal fade show" 
       style="display: block; background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEditing ? 'Edit Chapter' : 'Add New Chapter' }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <form @submit.prevent="saveChapter">
            <div class="mb-3">
              <label for="chapterName" class="form-label">Name</label>
              <input type="text" 
                     class="form-control" 
                     id="chapterName" 
                     v-model="chapterForm.name" 
                     required>
            </div>
            <div class="mb-3">
              <label for="chapterDescription" class="form-label">Description</label>
              <textarea class="form-control" 
                       id="chapterDescription" 
                       v-model="chapterForm.description" 
                       rows="3"></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" 
                  class="btn btn-secondary" 
                  @click="closeModal">Cancel</button>
          <button type="button" 
                  class="btn btn-primary" 
                  @click="saveChapter"
                  :disabled="!chapterForm.name">
            {{ isEditing ? 'Save Changes' : 'Create Chapter' }}
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
</style> 