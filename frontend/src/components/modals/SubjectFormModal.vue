<script setup>
import { ref, watch } from 'vue';
import api from '@/api';

const props = defineProps({
  show: Boolean,
  subject: Object,  
  isEditing: Boolean 
});

const emit = defineEmits(['close', 'subject-added', 'subject-updated']);

const error = ref('');
const subjectForm = ref({
  name: '',
  description: ''
});

// Watch both show and subject props
watch(
  [() => props.show, () => props.subject],
  ([newShow, newSubject]) => {
    if (newShow && props.isEditing && newSubject) {
      // Populate form when modal opens for editing
      subjectForm.value = {
        name: newSubject.name,
        description: newSubject.description
      };
    } else if (!newShow) {
      // Reset form when modal closes
      subjectForm.value = {
        name: '',
        description: ''
      };
    }
  }
);

const saveSubject = async () => {
  try {
    if (props.isEditing) {
      await api.put(`/admin/api/subjects/${props.subject.id}`, subjectForm.value);
      emit('subject-updated');
    } else {
      await api.post('/admin/api/subjects', subjectForm.value);
      emit('subject-added');
    }
    closeModal();
  } catch (err) {
    error.value = `Failed to ${props.isEditing ? 'update' : 'create'} subject.`;
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
          <h5 class="modal-title">{{ isEditing ? 'Edit Subject' : 'Add New Subject' }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <form @submit.prevent="saveSubject">
            <div class="mb-3">
              <label for="subjectName" class="form-label">Name</label>
              <input type="text" 
                     class="form-control" 
                     id="subjectName" 
                     v-model="subjectForm.name" 
                     required>
            </div>
            <div class="mb-3">
              <label for="subjectDescription" class="form-label">Description</label>
              <textarea class="form-control" 
                       id="subjectDescription" 
                       v-model="subjectForm.description" 
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
                  @click="saveSubject"
                  :disabled="!subjectForm.name">
            {{ isEditing ? 'Save Changes' : 'Create Subject' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template> 