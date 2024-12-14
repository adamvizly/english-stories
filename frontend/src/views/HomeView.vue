<template>
  <div class="home-container">
    <h1>Welcome to English Stories</h1>
    <p>Improve your English through interactive learning</p>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background-color: #f4f4f4;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.btn {
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 4px;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #2980b9;
}
</style>
