<template>
    <form @submit.prevent="handleSubmit" class="user-details-form"> 
        <!-- Prevent default reloading and call handleSubmit instead -->
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" v-model="formData.username" required/>
            <div v-if="errors.username" class="text-danger">{{ errors.username }}</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" v-model="formData.email" required/>
            <div v-if="errors.email" class="text-danger">{{ errors.email }}</div>

        </div>
        <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="text" class="form-control" v-model="formData.full_name" required/>
            <div v-if="errors.full_name" class="text-danger">{{ errors.full_name }}</div>

        </div>
        <div class="mb-3">
            <label class="form-label">Date of Birth</label>
            <input type="date" class="form-control" v-model="formData.date_of_birth"/>
            <div v-if="errors.date_of_birth" class="text-danger">{{ errors.date_of_birth }}</div>

        </div>
        <div class="mb-3">
            <label class="form-label">Qualification</label>
            <input type="text" class="form-control" v-model="formData.qualification"/>
        </div>
        <div v-if="isRegistering">
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="formData.password" required/>
                <div v-if="errors.password" class="text-danger">{{ errors.password }}</div>

            </div>
            <div class="mb-3">
                <label class="form-label">Confirm Password</label>
                <input type="password" class="form-control" v-model="formData.confirm_password" required/>
                <div v-if="errors.confirm_password" class="text-danger">{{ errors.confirm_password }}</div>

            </div>
        </div>
        <button type="submit" class="btn btn-primary">
            {{ isRegistering ? 'Register' : 'Update' }}
        </button>

    </form>

</template>
<script setup>
import { defineProps, defineEmits, reactive } from 'vue';

const props = defineProps({
    user: Object,
    isRegistering: Boolean
});

const emit = defineEmits(['submit']);

const formData = reactive({
    username: props.user?.username || '',
    email: props.user?.email || '',
    full_name: props.user?.full_name || '',
    date_of_birth: props.user?.date_of_birth || '',
    qualification: props.user?.qualification || '',
    password: '',
    confirm_password: ''
});

const errors = reactive({
    username: '',
    email: '',
    full_name: '',
    date_of_birth: '',
    password: '',
    confirm_password: ''
});

// validation functions
const validateData = () => {
    const unameRegex = /^[a-zA-Z0-9_]{3,50}$/;
    errors.username = unameRegex.test(formData.username)? '': 'Username must be 3-50 characters long and contain only letters, numbers, and underscores.';

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    errors.email = emailRegex.test(formData.email) ?'':'Please enter a valid email address.'

    const nameRegex = /^[A-Za-z\s]{3,}$/;
    errors.full_name = nameRegex.test(formData.full_name) ? '':'Name must be at least 3 characters long and contain only alphabets.'

    const enteredYear = new Date(formData.date_of_birth).getFullYear();
    const currentYear = new Date().getFullYear();
    errors.date_of_birth = enteredYear < currentYear ? '' : 'Date of birth must be before this year.';

    errors.password = formData.password.length >= 8? '': 'Password mult be atleast 8 characters long';
    errors.confirm_password = formData.password === formData.confirm_password ? '' : 'Passwords do not match.';

};


const handleSubmit = () => {
    validateData();
    if (Object.values(errors).some(error => error !== '')) {
        alert('Please fix the validation errors before submitting.');
        return;
    }
    if (props.isRegistering && formData.password !== formData.confirm_password) {
        alert('Passwords do not match');
        return;
    }
    emit('submit', formData);
};

</script>

<style scoped>
.user-details-form {
    background: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
}

.form-label {
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    display: block;
}

.form-control {
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
    font-size: 1rem;
}

.form-control:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.text-danger {
    color: #dc3545;
    font-size: 0.875rem;
    margin-top: 0.25rem;
    font-weight: 500;
}

.btn {
    border-radius: 50px;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    border: none;
    font-size: 1rem;
}

.btn-primary {
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.mb-3 {
    margin-bottom: 1.5rem;
}
</style>