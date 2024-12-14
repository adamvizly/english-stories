<script setup>
import { ref } from 'vue'
import LoginForm from '@/components/LoginForm.vue'
import SignupForm from '@/components/SignupForm.vue'

const isLoginMode = ref(true)
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-toggle">
        <button 
          @click="isLoginMode = true" 
          :class="{ active: isLoginMode }"
        >
          Login
        </button>
        <button 
          @click="isLoginMode = false" 
          :class="{ active: !isLoginMode }"
        >
          Sign Up
        </button>
      </div>
      
      <LoginForm v-if="isLoginMode" />
      <SignupForm v-else />
      
      <div class="auth-divider">
        <span>or</span>
      </div>
      
      <button class="google-auth">
        Continue with Google
      </button>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.auth-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
}

.auth-toggle {
  display: flex;
  margin-bottom: 20px;
}

.auth-toggle button {
  flex: 1;
  padding: 10px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-toggle button.active {
  background-color: #007bff;
  color: white;
}

.auth-divider {
  text-align: center;
  margin: 20px 0;
  position: relative;
}

.auth-divider span {
  background-color: white;
  padding: 0 10px;
  position: relative;
  z-index: 1;
}

.auth-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  border-top: 1px solid #ccc;
  z-index: 0;
}

.google-auth {
  width: 100%;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.google-auth:hover {
  background-color: #f0f0f0;
}
</style>
