<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2 class="login-title">Welcome Back</h2>
        <p class="login-subtitle">Sign in to your Quiz Master account</p>
      </div>
      
      <form @submit.prevent="loginUser" class="login-form">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input 
            type="text" 
            class="form-input" 
            id="username" 
            v-model="authData.username"
            placeholder="Enter your username"
          >
        </div>
        
        <div class="form-group">
          <label class="form-label">Password</label>
          <input 
            type="password" 
            class="form-input" 
            id="password" 
            v-model="authData.password"
            placeholder="Enter your password"
          >
        </div>
        
        <!-- <div class="form-options">
          <div class="checkbox-group">
            <input type="checkbox" class="form-checkbox" id="remember">
            <label class="checkbox-label" for="remember">Remember me</label>
          </div>
          <a href="#" class="forgot-link">Forgot password?</a>
        </div> -->
        
        <button type="submit" class="login-btn">
          <span>Sign In</span>
        </button>
        
        <div class="signup-link">
          <p>Don't have an account? 
            <router-link to="/register" class="link">Sign Up</router-link>
          </p>
        </div>
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
    const token = response.data.access_token;
    const role = response.data.role;
    
    authStore.login(token, role);
    router.push(role === 'admin' ? '/admin/home' : '/user/home');
  }catch(error){
    alert('Login Failed!!');
    console.log(error);
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #666;
  font-size: 1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #999;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-checkbox {
  width: 16px;
  height: 16px;
  accent-color: #667eea;
}

.checkbox-label {
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
}

.forgot-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #764ba2;
}

.login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.login-btn:active {
  transform: translateY(0);
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
}

.signup-link p {
  color: #666;
  margin: 0;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link:hover {
  color: #764ba2;
}

/* Responsive Design */
@media (max-width: 480px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-card {
    padding: 2rem;
  }
  
  .login-title {
    font-size: 1.75rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
