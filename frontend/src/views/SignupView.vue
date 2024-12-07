<template>
  <div class="signup-page">
    <div class="signup-container">
      <h1>Create an Account</h1>
      <p>Join English Stories today</p>
      
      <form @submit.prevent="handleSubmit" class="signup-form">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            type="text"
            id="name"
            v-model="name"
            required
            placeholder="Enter your name"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>

        <button type="submit" :disabled="authStore.loading" class="signup-button">
          {{ authStore.loading ? 'Loading...' : 'Sign Up' }}
        </button>
      </form>

      <div class="divider">
        <span>OR</span>
      </div>

      <div class="signup-buttons">
        <GoogleLogin :callback="handleGoogleLogin" />
      </div>

      <p v-if="authStore.error" class="error">{{ authStore.error }}</p>
      
      <p class="auth-link">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import { GoogleLogin } from 'vue3-google-login'

const authStore = useAuthStore()
const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')

const handleSubmit = async () => {
  try {
    await authStore.signup(email.value, password.value, name.value)
    router.push('/')
  } catch (error) {
    console.error('Signup failed:', error)
  }
}

const handleGoogleLogin = async (response) => {
  try {
    await authStore.loginWithGoogle(response.credential)
    router.push('/')
  } catch (error) {
    console.error('Google login failed:', error)
  }
}
</script>

<style scoped>
.signup-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.signup-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1.5rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: left;
}

label {
  font-weight: 500;
  color: #2c3e50;
}

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.signup-button {
  padding: 0.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.signup-button:disabled {
  background-color: #ccc;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #ddd;
}

.divider span {
  padding: 0 10px;
  color: #666;
  font-size: 0.9rem;
}

.signup-buttons {
  margin-top: 1rem;
}

.error {
  color: #dc3545;
  margin-top: 1rem;
}

.auth-link {
  margin-top: 1rem;
  color: #666;
}

.auth-link a {
  color: #4CAF50;
  text-decoration: none;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>
