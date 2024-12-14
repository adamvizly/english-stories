<template>
  <nav v-if="isAuthenticated" class="nav">
    <router-link to="/" class="nav-link">Home</router-link>
    <router-link to="/stories" class="nav-link">Stories</router-link>
    <router-link to="/daily-words" class="nav-link">Daily Words</router-link>
    <a href="#" @click="logout" class="nav-link logout">Logout</a>
  </nav>
  <router-view/>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './store/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

.nav {
  background: #2c3e50;
  padding: 1rem;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #34495e;
}

.router-link-active {
  background-color: #34495e;
}

.logout {
  color: #e74c3c;
}

.logout:hover {
  background-color: #c0392b;
  color: white;
}
</style>
