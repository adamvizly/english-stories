<template>
  <div class="home">
    <header class="hero">
      <h1>Welcome to English Stories</h1>
      <p>Improve your English through interactive stories and grammar lessons</p>
    </header>
    
    <main class="features">
      <div class="feature-card" @click="router.push('/stories')">
        <h2>Stories</h2>
        <p>Read and learn from AI-generated stories tailored to your level</p>
      </div>
      
      <div class="feature-card" @click="router.push('/grammar')">
        <h2>Grammar</h2>
        <p>Get personalized grammar hints and practice exercises</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(to right, #3498db, #2ecc71);
  color: white;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}
</style>
