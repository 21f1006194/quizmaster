<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">Quiz Master</router-link>
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <!-- Not authenticated users -->
            <template v-if="!authStore.isAuthenticated">
              <li class="nav-item">
                <router-link class="nav-link" to="/">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/about">About</router-link>
              </li>
            </template>

            <!-- Admin users -->
            <template v-if="authStore.isAuthenticated && authStore.role === 'admin'">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/home">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/quiz">Quiz</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/users">Users</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/summary">Summary</router-link>
              </li>
            </template>

            <!-- Regular users -->
            <template v-if="authStore.isAuthenticated && authStore.role !== 'admin'">
              <li class="nav-item">
                <router-link class="nav-link" to="/user/home">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/user/result">Result</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/user/summary">Summary</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/user/profile">Profile</router-link>
              </li>
            </template>
          </ul>
          <ul class="navbar-nav">
            <li v-if="!authStore.isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li v-if="authStore.isAuthenticated" class="nav-item">
              <button class="btn btn-danger" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/authStore';
  
  const authStore = useAuthStore();
  const router = useRouter();
  
  const logout = () => {
    authStore.logout();
    router.push('/login'); 
  };
  </script>
  
  <style scoped>
  .navbar {
    margin-bottom: 20px;
  }
  </style>
  