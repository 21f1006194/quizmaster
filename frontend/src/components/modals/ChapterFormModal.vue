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