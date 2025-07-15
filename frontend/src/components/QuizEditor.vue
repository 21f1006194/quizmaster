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
  <div>
    <QuillEditor
      ref="editor"
      :options="editorOptions"
      @text-change="onEditorChange"
    />
  </div>
</template>

<style>
.ql-editor {
  min-height: 200px;
}
</style>
