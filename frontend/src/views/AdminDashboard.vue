<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import { fetchCatalogData } from '@/utils/catalogData';
import SubjectFormModal from '@/components/modals/SubjectFormModal.vue';
import ChapterFormModal from '@/components/modals/ChapterFormModal.vue';

const router = useRouter();

const subjects = ref({ subjects: [] });
const loading = ref(false);
const error = ref('');
const showSubjectModal = ref(false);
const showChapterModal = ref(false);
const selectedChapter = ref(null);
const selectedSubject = ref(null);
const isEditingSubject = ref(false);
const isEditingChapter = ref(false);

const loadData = async () => {
  loading.value = true;
  try {
    const { data, error: fetchError } = await fetchCatalogData();
    if (fetchError) throw new Error(fetchError);
    subjects.value = data;
  } catch (err) {
    error.value = 'Failed to fetch subjects.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const deleteChapter = async (chapterId) => {
  try {
    const response = await api.delete(`/admin/api/chapters/${chapterId}`);
    if (response.status === 200) {
      await loadData();
    }
  } catch (err) {
    error.value = err.response?.data?.msg || 'Failed to delete chapter.';
    console.error(err);
  }
};

const deleteSubject = async (subjectId) => {
  try {
    console.log(`Deleting subject: ${subjectId}`);
    const response = await api.delete(`/admin/api/subjects/${subjectId}`);
    if (response.status === 200) {
      await loadData();
    }
  } catch (err) {
    error.value = err.response?.data?.msg || 'Failed to delete subject.';
    console.error(err);
  }
};

const openSubjectModal = (subject = null) => {
  selectedSubject.value = subject;
  isEditingSubject.value = !!subject;
  showSubjectModal.value = true;
};

const openChapterModal = (subject, chapter = null) => {
  selectedSubject.value = subject;
  selectedChapter.value = chapter;
  isEditingChapter.value = !!chapter;
  showChapterModal.value = true;
};

const navigateToQuizzes = (subject, chapter) => {
  const searchQuery = `subject:${subject.name} chapter:${chapter.name}`;
  router.push({
    name: 'adminQuiz',
    query: { search: searchQuery }
  });
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="admin-dashboard">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="dashboard-title">Admin Dashboard</h1>
        <div v-if="loading" class="alert alert-info">Loading subjects...</div>
        <div v-if="error" class="alert alert-danger alert-dismissible fade show">
          {{ error }}
          <button type="button" class="btn-close" @click="error = ''" aria-label="Close"></button>
        </div>
        <button class="btn btn-primary rounded-pill" @click="openSubjectModal()">
          <i class="bi bi-plus-circle"></i> Subject
        </button>
      </div>
      <div v-if="subjects.subjects && subjects.subjects.length" class="row g-4">
        <div v-for="subject in subjects.subjects" :key="subject.id" class="col-md-6 col-lg-4">
          <div class="card h-100 subject-card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h3 class="card-title mb-0">{{ subject.name }}</h3>
              <div class="btn-group">
                <button class="btn btn-link p-0 me-3" @click="openSubjectModal(subject)" title="Edit Subject">
                  <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn btn-link p-0 " @click="deleteSubject(subject.id)" title="Delete Subject">
                  <i class="bi bi-trash3"></i>
                </button>
              </div>
            </div>
            <div class="card-body">            
               <ul class="list-group list-group-flush">
                <li v-for="chapter in subject.chapters" :key="chapter.id" 
                    class="list-group-item list-group-item-action shadow-sm border-0 mb-2 transition-all d-flex justify-content-between align-items-center chapter-row"
                    @click="navigateToQuizzes(subject, chapter)"
                >
                  <span>{{ chapter.name }} ({{ chapter.quizzes.length }})</span>
                  <div class="btn-group" @click.stop>
                    <button @click="openChapterModal(subject, chapter)" 
                            class="btn btn-sm btn-outline-primary">
                      Edit
                    </button>
                    <button @click="deleteChapter(chapter.id)" 
                            class="btn btn-sm btn-outline-danger">
                      Delete
                    </button>
                  </div>
                </li>
              </ul>
            </div>
            <div class="card-footer">
              <button class="btn btn-primary w-100" 
                      @click="openChapterModal(subject)">
                  Add New Chapter
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modals -->
      <SubjectFormModal 
        :show="showSubjectModal"
        :subject="selectedSubject"
        :is-editing="isEditingSubject"
        @close="showSubjectModal = false"
        @subject-added="loadData"
        @subject-updated="loadData"
      />

      <ChapterFormModal
        :show="showChapterModal"
        :chapter="selectedChapter"
        :subject-id="selectedSubject?.id"
        :is-editing="isEditingChapter"
        @close="showChapterModal = false"
        @chapter-added="loadData"
        @chapter-updated="loadData"
      />
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem 0;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0;
}

.subject-card {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  border-radius: 20px;
  transition: all 0.3s ease;
  background: white;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px 20px 0 0 !important;
  border-bottom: none;
}

.card-title {
  color: white;
  font-weight: 600;
}

.btn-group {
  gap: 0.5rem;
}

.btn-link {
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.btn-link:hover {
  color: white;
  transform: scale(1.1);
}

.chapter-row {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 10px;
  margin-bottom: 0.5rem;
}

.chapter-row:hover {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transform: translateX(5px);
}

.btn {
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
  background: transparent;
}

.btn-outline-primary:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.btn-outline-danger {
  border: 2px solid #dc3545;
  color: #dc3545;
  background: transparent;
}

.btn-outline-danger:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-1px);
}

.btn-sm {
  padding: 0.375rem 1rem;
  font-size: 0.875rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1050;
}

.modal-dialog {
  margin: 1.75rem auto;
}

.btn-group {
  z-index: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-title {
    font-size: 2rem;
  }
  
  .admin-dashboard {
    padding: 1rem 0;
  }
}
</style>
