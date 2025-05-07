<template>

<div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-lg" style="width: 400px;">
      <h3 class="text-center mb-4">Login</h3>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" class="form-control" id="username" v-model="authData.username">
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="authData.password">
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <div class="form-check">
            <input type="checkbox" class="form-check-input" id="remember">
            <label class="form-check-label" for="remember">Remember me</label>
          </div>
          <a href="#" class="text-decoration-none">Forgot password?</a>
        </div>
        <div class="d-grid mt-4">
          <button type="submit" class="btn btn-primary">Login</button>
        </div>
        <p class="text-center mt-3 mb-0">
          Don't have an account? 
          <router-link to="/register" class="text-decoration-none">Sign Up</router-link>
        </p>
      </form>
    </div>
  </div>

</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { reactive } from 'vue';
import api from '@/api'

const authData = reactive({
  username: '',
  password: ''
})

const router = useRouter();
const authStore = useAuthStore();

const loginUser = async ()=>{
  try{
    const response = await api.post('/api/login', authData);
    alert('Login successful');
    const token = response.data.access_token;
    const role = response.data.role;
    
    authStore.login(token, role);
    router.push(role === 'admin' ? '/admin/dashboard' : '/user/dashboard');
  }catch(error){
    alert('Login Failed!!');
    console.log(error);
  }
}
</script>
