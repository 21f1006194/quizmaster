<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';

const props = defineProps({
  show: Boolean,
  quizDetails: Object,
  mode: {
    type: String,
    default: 'edit', // 'edit' or 'create'
  }
});

const router = useRouter();
const emit = defineEmits(['close', 'quiz-updated', 'update:modelValue']);

const subjects = ref([]);
const formData = ref({
  title: '',
  quiz_date: '',
  time_duration: 0,
  remarks: '',
  subject_id: '',
  chapter_id: '',
});

const availableChapters = ref([]);

// Helper function to find subject ID from chapter ID
const findSubjectByChapterId = (chapterId) => {
  for (const subject of subjects.value) {
    const chapter = subject.chapters.find(ch => ch.id === chapterId);
    if (chapter) {
      return subject.id;
    }
  }
  return null;
};

const loadSubjects = async () => {
  try {
    const response = await api.get('/admin/api/subjects');
    subjects.value = response.data.subjects;
    
    // If we have quiz details, set the subject and chapter
    if (props.quizDetails) {
      const subjectId = findSubjectByChapterId(props.quizDetails.chapter_id);
      if (subjectId) {
        formData.value.subject_id = subjectId;
        handleSubjectChange();
        formData.value.chapter_id = props.quizDetails.chapter_id;
      }
    }
  } catch (error) {
    console.error('Error loading subjects:', error);
  }
};

const handleSubjectChange = () => {
  const selectedSubject = subjects.value.find(s => s.id === formData.value.subject_id);
  availableChapters.value = selectedSubject?.chapters || [];
  if (!availableChapters.value.find(c => c.id === formData.value.chapter_id)) {
    formData.value.chapter_id = '';
  }
};

const handleSubmit = async () => {
  try {
    if (props.mode === 'edit') {
      await api.put(`/admin/api/quiz/${props.quizDetails.quiz_id}`, formData.value);
      emit('quiz-updated');
    } else {
      // Create new quiz
      const response = await api.post(`/admin/api/chapters/${formData.value.chapter_id}/quiz`, {
        title: formData.value.title,
        quiz_date: formData.value.quiz_date,
        time_duration: formData.value.time_duration,
        remarks: formData.value.remarks
      });
      
      // First check if we have a valid quiz id
      console.log(response.data);
      if (response.data && response.data.id) {
        emit('close');
        // Only redirect after confirming we have a valid quiz id
        router.push(`/admin/quiz-edit/${response.data.id}`);
      } else {
        throw new Error('Failed to get quiz ID from response');
      }
      return;
    }
    emit('close');
  } catch (error) {
    console.error('Error saving quiz:', error);
    alert('Failed to save quiz');
  }
};

// Function to format date-time to IST
const formatToIST = (dateString) => {
  const date = new Date(dateString);
  // Convert to IST (UTC+5:30)
  const istOptions = {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  };
  
  const istDateTime = new Intl.DateTimeFormat('en-IN', istOptions)
    .format(date)
    .replace(/(\d{2})\/(\d{2})\/(\d{4}), (\d{2}):(\d{2})/, '$3-$2-$1T$4:$5');
    
  return istDateTime;
};

// Watch for quiz details changes and set default values
watch(() => props.quizDetails, (newDetails) => {
  if (newDetails) {
    formData.value = {
      title: newDetails.quiz_title,
      quiz_date: formatToIST(newDetails.quiz_date),
      time_duration: newDetails.time_duration,
      remarks: newDetails.remarks || '',
      chapter_id: newDetails.chapter_id,
      subject_id: findSubjectByChapterId(newDetails.chapter_id) || ''
    };
  }
}, { immediate: true });

watch(() => props.show, (newVal) => {
  if (newVal && props.quizDetails) {
    // Refresh the form data when modal is shown
    formData.value = {
      title: props.quizDetails.quiz_title,
      quiz_date: formatToIST(props.quizDetails.quiz_date),
      time_duration: props.quizDetails.time_duration,
      remarks: props.quizDetails.remarks || '',
      chapter_id: props.quizDetails.chapter_id,
      subject_id: findSubjectByChapterId(props.quizDetails.chapter_id) || ''
    };
  }
});

onMounted(() => {
  loadSubjects();
});
</script>

<template>
  <div v-if="show" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg" style="max-width: 800px;">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ mode === 'edit' ? 'Edit Quiz Details' : 'Create New Quiz' }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit" class="row g-3">
            <div class="col-12">
              <label class="form-label">Title</label>
              <input type="text" class="form-control" v-model="formData.title" required>
            </div>
            
            <div class="col-md-6">
              <label class="form-label">Quiz Date</label>
              <input type="datetime-local" class="form-control" v-model="formData.quiz_date" required>
            </div>

            <div class="col-md-6">
              <label class="form-label">Duration (minutes)</label>
              <input type="number" class="form-control" v-model="formData.time_duration" required>
            </div>

            <div class="col-md-6">
              <label class="form-label">Subject</label>
              <select class="form-select" v-model="formData.subject_id" @change="handleSubjectChange" required>
                <option value="">Select Subject</option>
                <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                  {{ subject.name }}
                </option>
              </select>
            </div>

            <div class="col-md-6">
              <label class="form-label">Chapter</label>
              <select class="form-select" v-model="formData.chapter_id" required>
                <option value="">Select Chapter</option>
                <option v-for="chapter in availableChapters" :key="chapter.id" :value="chapter.id">
                  {{ chapter.name }}
                </option>
              </select>
            </div>

            <div class="col-12">
              <label class="form-label">Remarks</label>
              <textarea class="form-control" v-model="formData.remarks" rows="3"></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="button" class="btn btn-primary" @click="handleSubmit">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  z-index: 1050;
}

.modal-body {
  padding: 1.5rem;
}

.form-label {
  font-weight: 500;
}
</style> 