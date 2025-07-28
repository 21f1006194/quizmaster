<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2 class="register-title">Create Account</h2>
        <p class="register-subtitle">Join Quiz Master and start your learning journey</p>
      </div>
      
      <div class="register-form">
        <UserDetailsForm
          :isRegistering="true"
          @submit="registerUser"
        ></UserDetailsForm>
        
        <div class="login-link">
          <p>Already have an account?
            <router-link to="/login" class="link">Login here</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { useRouter } from 'vue-router';
import UserDetailsForm from '@/components/UserDetailsForm.vue';
import api from '@/api';

const router = useRouter();

const registerUser = async (formData) => {
    try {
        const response = await api.post('/api/register', formData);
        alert('Registration successful');
        router.push('/login');
    } catch (error) {
        console.error(error);
        alert('An error occurred');
    }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.register-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.register-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.register-subtitle {
  color: #666;
  font-size: 1rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e1e5e9;
}

.login-link p {
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
  .register-container {
    padding: 1rem;
  }
  
  .register-card {
    padding: 2rem;
  }
  
  .register-title {
    font-size: 1.75rem;
  }
}
</style>
  
  