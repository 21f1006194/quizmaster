<script setup>
import { ref, onMounted } from 'vue';
import { fetchCatalogData } from '@/utils/catalogData';
import SubjectFormModal from '@/components/modals/SubjectFormModal.vue';
import ChapterFormModal from '@/components/modals/ChapterFormModal.vue';

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

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-4">Admin Dashboard</h1>
      <div v-if="loading" class="alert alert-info">Loading subjects...</div>
      <div v-if="error" class="alert alert-danger alert-dismissible fade show">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''" aria-label="Close"></button>
      </div>
      <button class="btn btn-success rounded-pill" @click="openSubjectModal()" style="background-color: pink; border-color: pink; color: black;">
        <i class="bi bi-plus-circle"></i> Subject
      </button>
    </div>
    <div v-if="subjects.subjects && subjects.subjects.length" class="row g-4">
      <div v-for="subject in subjects.subjects" :key="subject.id" class="col-md-6 col-lg-4">
        <div class="card h-100">
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
                  class="list-group-item list-group-item-action shadow-sm border-0 mb-2 transition-all d-flex justify-content-between align-items-center">
                <span>{{ chapter.name }} ({{ chapter.quizzes.length }})</span>
                <div class="btn-group">
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
</template>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  background-color: #f8f9fa;
}

.btn-group {
  gap: 0.5rem;
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

.btn-link {
  color: #6c757d;
}

.btn-link:hover {
  color: #0d6efd;
}
</style>
