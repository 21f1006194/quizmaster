<script setup>
import { ref, watch, onMounted } from 'vue';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import ImageResize from 'quill-image-resize-module-plus';
import Quill from 'quill';

Quill.register('modules/imageResize', ImageResize);

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

const editor = ref(null);

// Initialize editor content on mount
onMounted(() => {
  if (editor.value && props.modelValue) {
    editor.value.setHTML(props.modelValue);
  }
});

// Only update editor content when modelValue changes from outside
watch(() => props.modelValue, (newContent) => {
  if (editor.value && newContent !== editor.value.getHTML()) {
    editor.value.setHTML(newContent);
  }
}, { deep: true });

const editorOptions = {
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline'],
      ['blockquote', 'code-block'],
      [{ list: 'ordered' }, { list: 'bullet' }],
      [{ script: 'sub' }, { script: 'super' }],
      ['link', 'image', 'imageURL'],
    ],
    imageResize: {
      modules: ['Resize', 'DisplaySize', 'Toolbar']
    },
  },
  theme: 'snow'
};

const onEditorChange = (delta) => {
  if (editor.value && delta.source === 'user') {
    const content = editor.value.getHTML();
    emit('update:modelValue', content);

  }
};
</script>

<template>
  <div class="quiz-editor-container">
    <QuillEditor
      ref="editor"
      :options="editorOptions"
      @text-change="onEditorChange"
    />
  </div>
</template>

<style>
.quiz-editor-container {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.quiz-editor-container:focus-within {
  border-color: #667eea;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
}

.ql-toolbar {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 2px solid #e0e0e0;
  border-top: none;
  border-left: none;
  border-right: none;
}

.ql-editor {
  min-height: 200px;
  padding: 1rem;
  font-size: 1rem;
  line-height: 1.6;
}

.ql-editor:focus {
  outline: none;
}

.ql-editor p {
  margin-bottom: 0.5rem;
}

.ql-editor h1, .ql-editor h2, .ql-editor h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.ql-editor blockquote {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: #666;
}

.ql-editor code {
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

.ql-editor pre {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}

.ql-editor img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 0.5rem 0;
}
</style>
