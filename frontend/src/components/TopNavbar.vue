<template>
  <nav class="top-navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        English Stories
      </router-link>
      
      <div class="nav-links">
        <router-link 
          v-for="route in navRoutes" 
          :key="route.name" 
          :to="route.path" 
          class="nav-link"
          active-class="active"
        >
          {{ route.name }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
const navRoutes = [
  { name: 'Home', path: '/' },
  { name: 'Stories', path: '/stories' },
  { name: 'Words', path: '/words' }
]
</script>

<style scoped>
.top-navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: bold;
}
</style>
