<script setup>

const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div>
    <h1>Welcome to the Quiz App</h1>
    <p>
      This is a simple quiz app built with Vue 3 and Vite.
    </p>
    <p>
      <button @click="openReadmeInEditor">Open README.md in Editor</button>
    </p>
  </div>
</template>
