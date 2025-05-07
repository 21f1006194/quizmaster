<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow-lg">
            <div class="card-body">
              <h3 class="text-center mb-4">Register</h3>
              <UserDetailsForm
                :isRegistering="true"
                @submit="registerUser"
              ></UserDetailsForm>
              <p class="text-center mt-3">
                Already have an account?
                <router-link to="/login">Login here</router-link>
              </p>
            </div>
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
  
  