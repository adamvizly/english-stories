<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Welcome to English Stories</h1>
      <p>Please sign in to continue</p>
      <div class="login-buttons">
        <GoogleLogin :callback="handleGoogleLogin" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import { GoogleLogin } from 'vue3-google-login'

const authStore = useAuthStore()
const router = useRouter()

const handleGoogleLogin = async (response) => {
  const success = await authStore.loginWithGoogle(response.credential)
  if (success) {
    router.push('/')
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.login-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.login-buttons {
  margin-top: 2rem;
}
</style>
