<template>
  <nav class="nav">
    <router-link to="/" class="nav-link">Stories</router-link>
    <router-link to="/words" class="nav-link">Words</router-link>
  </nav>
  <router-view/>
</template>

<script setup>
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
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #34495e;
}
</style>
