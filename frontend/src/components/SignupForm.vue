<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup } from '@/services/auth'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')

const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    await signup(email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Signup failed'
  }
}
</script>

<template>
  <form @submit.prevent="handleSignup" class="signup-form">
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
        placeholder="Create a password"
      />
    </div>
    
    <div class="form-group">
      <label for="confirm-password">Confirm Password</label>
      <input 
        type="password" 
        id="confirm-password" 
        v-model="confirmPassword" 
        required 
        placeholder="Confirm your password"
      />
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <button type="submit" class="signup-button">
      Sign Up
    </button>
  </form>
</template>

<style scoped>
.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error-message {
  color: red;
  margin-bottom: 15px;
  text-align: center;
}

.signup-button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.signup-button:hover {
  background-color: #218838;
}
</style>
