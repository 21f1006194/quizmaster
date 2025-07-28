<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Logo and Brand -->
      <router-link class="navbar-brand" to="/">
        <div class="brand-content">
          <img src="/qm_logo.png" alt="Quiz Master Logo" class="brand-logo" />
          <span class="brand-title">Quiz Master</span>
        </div>
      </router-link>

      <!-- Mobile Menu Toggle -->
      <button 
        class="navbar-toggle" 
        @click="toggleMobileMenu"
        :class="{ 'active': isMobileMenuOpen }"
      >
        <span class="toggle-line"></span>
        <span class="toggle-line"></span>
        <span class="toggle-line"></span>
      </button>

      <!-- Navigation Menu -->
      <div class="navbar-menu" :class="{ 'active': isMobileMenuOpen }">
        <ul class="nav-list">
          <!-- Not authenticated users -->
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/" @click="closeMobileMenu">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about" @click="closeMobileMenu">About</router-link>
            </li>
          </template>

          <!-- Admin users -->
          <template v-if="authStore.isAuthenticated && authStore.role === 'admin'">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/home" @click="closeMobileMenu">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/quiz" @click="closeMobileMenu">Manage Quiz</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/users" @click="closeMobileMenu">Users</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/summary" @click="closeMobileMenu">Summary</router-link>
            </li>
          </template>

          <!-- Regular users -->
          <template v-if="authStore.isAuthenticated && authStore.role !== 'admin'">
            <li class="nav-item">
              <router-link class="nav-link" to="/user/home" @click="closeMobileMenu">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/user/result" @click="closeMobileMenu">Results</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/user/summary" @click="closeMobileMenu">Summary</router-link>
            </li>
          </template>
        </ul>

        <!-- Auth Buttons -->
        <div class="auth-buttons">
          <template v-if="!authStore.isAuthenticated">
            <router-link class="auth-btn auth-btn-login" to="/login" @click="closeMobileMenu">
              Login
            </router-link>
            <router-link class="auth-btn auth-btn-register" to="/register" @click="closeMobileMenu">
              Register
            </router-link>
          </template>
          <template v-else>
            <button class="auth-btn auth-btn-logout" @click="logout">
              Logout
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const logout = () => {
  authStore.logout()
  router.push('/login')
  closeMobileMenu()
}
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0.75rem 0;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

/* Brand/Logo */
.navbar-brand {
  text-decoration: none;
  color: inherit;
  flex-shrink: 0;
}

.brand-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.brand-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Mobile Toggle */
.navbar-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  gap: 4px;
}

.toggle-line {
  width: 25px;
  height: 3px;
  background: #667eea;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.navbar-toggle.active .toggle-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.navbar-toggle.active .toggle-line:nth-child(2) {
  opacity: 0;
}

.navbar-toggle.active .toggle-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Navigation Menu */
.navbar-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-left: auto;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1.5rem;
}

.nav-item {
  position: relative;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #667eea;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

/* Auth Buttons */
.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.auth-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.auth-btn-login {
  color: #667eea;
  background: transparent;
  border: 2px solid #667eea;
}

.auth-btn-login:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.auth-btn-register {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.auth-btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.auth-btn-logout {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.auth-btn-logout:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-toggle {
    display: flex;
  }

  .navbar-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    flex-direction: column;
    padding: 2rem;
    gap: 1.5rem;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  }

  .navbar-menu.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav-list {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .nav-link {
    display: block;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  }

  .nav-link::after {
    display: none;
  }

  .auth-buttons {
    flex-direction: column;
    width: 100%;
    gap: 0.75rem;
  }

  .auth-btn {
    width: 100%;
    text-align: center;
    padding: 0.75rem 1.5rem;
  }

  .brand-title {
    font-size: 1.25rem;
  }

  .brand-logo {
    width: 35px;
    height: 35px;
  }
}

@media (max-width: 480px) {
  .navbar-container {
    padding: 0 1rem;
  }

  .brand-content {
    gap: 0.5rem;
  }

  .brand-title {
    font-size: 1.1rem;
  }

  .brand-logo {
    width: 30px;
    height: 30px;
  }
}
</style>
  